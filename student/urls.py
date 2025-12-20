from django.urls import path
from .views import student_profile

urlpatterns = [
    path('profile/<int:user_id>/', student_profile),
]