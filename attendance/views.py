from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.timezone import now
from .models import Attendance
from .serializers import AttendanceSerializer
from student.models import Student
from academics.models import Subject, Hour
from django.db.models import Count, Q


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




@api_view(['GET'])
def student_dashboard(request, student_id):
    try:
        student = Student.objects.get(id=student_id)

        total_classes = Attendance.objects.filter(student=student).count()
        present_count = Attendance.objects.filter(
            student=student, status=Attendance.PRESENT
        ).count()
        absent_count = Attendance.objects.filter(
            student=student, status=Attendance.ABSENT
        ).count()

        percentage = 0
        if total_classes > 0:
            percentage = round((present_count / total_classes) * 100, 2)

        # Subject-wise stats
        subject_stats = (
            Attendance.objects
            .filter(student=student)
            .values('subject__name')
            .annotate(
                total=Count('id'),
                present=Count('id', filter=Q(status=Attendance.PRESENT))
            )
        )

        return Response({
            "student": student.roll_number,
            "total_classes": total_classes,
            "present_days": present_count,
            "absent_days": absent_count,
            "attendance_percentage": percentage,
            "subject_wise": subject_stats
        })

    except Student.DoesNotExist:
        return Response({"error": "Student not found"}, status=404)
