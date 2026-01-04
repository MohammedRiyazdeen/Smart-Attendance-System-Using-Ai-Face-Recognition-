from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )

    roll_number = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    year = models.PositiveIntegerField()

    # Placeholder for AI face data (encoding path or ID)
    face_data = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"{self.roll_number} - {self.user.username}"

