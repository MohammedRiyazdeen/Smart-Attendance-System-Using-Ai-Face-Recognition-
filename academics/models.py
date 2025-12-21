from django.db import models

# Create your models here.

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f'{self.nmae} ({self.code})'
    
    
