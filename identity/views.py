from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .serializers import UserSerializer

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user:
        return Response({
            "message": "Login successful",
            "user": UserSerializer(user).data
        })
    return Response({"error": "Invalid credentials"}, status=400)
