from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistrationSerializer, LoginSerializer
from auth_app.models import UserProfile


class RegistrationView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, req):
        serializer = RegistrationSerializer(data=req.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            UserProfile.objects.create(user=user, user_type=req.data["type"])
            data = {
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "user_id": user.pk
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, req):
        serializer = LoginSerializer(data=req.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)
            data = {
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "user_id": user.pk
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)