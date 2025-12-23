from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistrationSerializer, LoginSerializer, ProfileSerializer, BusinessProfileSerializer, CustomerProfileSerializer
from auth_app.models import UserProfile
from .permissions import IsProfileOwner


class RegistrationView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, req):
        serializer = RegistrationSerializer(data=req.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            UserProfile.objects.create(user=user, type=req.data["type"])
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
    
    
class ProfileRetrievePatchView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsProfileOwner]
    
    
class ProfileListView(generics.ListAPIView):
    def get_queryset(self):
        if "business" in self.request.get_full_path():
            return UserProfile.objects.filter(type="business")
        if "customer" in self.request.get_full_path():
            return UserProfile.objects.filter(type="customer")
        
    def get_serializer_class(self):
        if "business" in self.request.get_full_path():
            return BusinessProfileSerializer
        if "customer" in self.request.get_full_path():
            return CustomerProfileSerializer