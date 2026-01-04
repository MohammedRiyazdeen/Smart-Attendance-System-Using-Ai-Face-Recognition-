from django.urls import path
from .views import mark_attendance, student_dashboard

urlpatterns = [
    path('mark/', mark_attendance),
    path('student-dashboard/<int:student_id>/', student_dashboard),
]
