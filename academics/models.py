from django.db import models

# Create your models here.

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.name} ({self.code})"
    

class Hour(models.Model):
    hour_number = models.PositiveIntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"Hour {self.hour_number}"


class Timetable(models.Model):
    DAYS = [
        ('mon', 'Monday'),
        ('tue', 'Tuesday'),
        ('wed', 'Wednesday'),
        ('thu', 'Thursday'),
        ('fri', 'Friday'),
    ]

    day = models.CharField(max_length=3, choices=DAYS)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    hour = models.ForeignKey(Hour, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('day', 'hour')

    def __str__(self):
        return f"{self.day} - {self.subject} - Hour {self.hour.hour_number}"
