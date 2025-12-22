from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.timezone import now
from .models import Attendance
from .serializers import AttendanceSerializer
from student.models import Student
from academics.models import Subject, Hour

@api_view(['POST'])
def mark_attendance(request):
    student_id = request.data.get('student_id')
    subject_id = request.data.get('subject_id')
    hour_id = request.data.get('hour_id')

    today = now().date()

    try:
        student = Student.objects.get(id=student_id)
        subject = Subject.objects.get(id=subject_id)
        hour = Hour.objects.get(id=hour_id)

        attendance, created = Attendance.objects.get_or_create(
            student=student,
            subject=subject,
            hour=hour,
            date=today,
            defaults={'status': Attendance.PRESENT}
        )

        if not created:
            return Response(
                {"message": "Attendance already marked"},
                status=400
            )

        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data)

    except Exception as e:
        return Response({"error": str(e)}, status=400)
