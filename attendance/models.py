from django.db import models
from student.models import Student
from academics.models import Subject, Hour
from identity.models import Teacher


class AttendanceSession(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    hour = models.ForeignKey(Hour, on_delete=models.CASCADE)

    date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.teacher} | {self.subject} | {self.date} | {self.hour}"


class Attendance(models.Model):
    PRESENT = 'present'
    ABSENT = 'absent'

    STATUS_CHOICES = [
        (PRESENT, 'Present'),
        (ABSENT, 'Absent'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PRESENT
    )
    marked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'session')  # 🔒 correct duplicate lock

    def __str__(self):
        return f"{self.student} | {self.session} | {self.status}"
