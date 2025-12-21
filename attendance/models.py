from django.db import models
from student.models import Student
from academics.models import Subject, Hour

class Attendance(models.Model):
    PRESENT = 'present'
    ABSENT = 'absent'

    STATUS_CHOICES = [
        (PRESENT, 'Present'),
        (ABSENT, 'Absent'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    hour = models.ForeignKey(Hour, on_delete=models.CASCADE)

    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('student', 'date', 'hour')

    def __str__(self):
        return f"{self.student.roll_number} | {self.date} | Hour {self.hour.hour_number}"
