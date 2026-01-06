from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Attendance, AttendanceSession
from .serializers import AttendanceSerializer

from student.models import Student
from identity.models import Teacher


@api_view(['POST'])
def start_attendance_session(request):
    teacher_id = request.data.get('teacher_id')
    subject_id = request.data.get('subject_id')
    hour_id = request.data.get('hour_id')

    try:
        teacher = Teacher.objects.get(id=teacher_id)

        # Close any previous active session
        AttendanceSession.objects.filter(
            teacher=teacher,
            is_active=True
        ).update(is_active=False)

        session = AttendanceSession.objects.create(
            teacher=teacher,
            subject_id=subject_id,
            hour_id=hour_id
        )

        return Response({
            "session_id": session.id,
            "message": "Attendance session started"
        })

    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(['POST'])
def mark_attendance(request):
    student_id = request.data.get('student_id')
    session_id = request.data.get('session_id')

    if not student_id or not session_id:
        return Response(
            {"error": "student_id and session_id required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        student = Student.objects.get(id=student_id)
        session = AttendanceSession.objects.get(id=session_id)

        if not session.is_active:
            return Response(
                {"error": "Attendance session is closed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        attendance, created = Attendance.objects.get_or_create(
            student=student,
            session=session
        )

        if not created:
            return Response(
                {"message": "Attendance already marked"},
                status=status.HTTP_200_OK
            )

        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": str(e)}, status=400)
