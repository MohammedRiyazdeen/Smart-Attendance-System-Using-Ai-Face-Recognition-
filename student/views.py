from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Student
from .serializers import StudentSerializer

@api_view(['GET'])
def student_profile(request, user_id):
    try:
        student = Student.objects.get(user__id=user_id)
        serializer = StudentSerializer(student)
        return Response(serializer.data)
    except Student.DoesNotExist:
        return Response(
            {"error": "Student profile not found"},
            status=404
        )

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Student

@api_view(['POST'])
def save_face_data(request):
    student_id = request.data.get('student_id')
    face_path = request.data.get('face_path')

    try:
        student = Student.objects.get(id=student_id)
        student.face_data = face_path
        student.save()
        return Response({"message": "Face data linked successfully"})
    except Student.DoesNotExist:
        return Response({"error": "Student not found"}, status=404)
