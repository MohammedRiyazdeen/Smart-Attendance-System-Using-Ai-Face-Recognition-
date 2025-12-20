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
