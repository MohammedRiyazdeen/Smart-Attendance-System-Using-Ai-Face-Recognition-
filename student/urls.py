from django.urls import path
from .views import student_profile, save_face_data

urlpatterns = [
    path('profile/<int:user_id>/', student_profile),
    path('save-face/', save_face_data),

]