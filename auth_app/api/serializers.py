from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate


class RegistrationSerializer(serializers.ModelSerializer):
    
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.CharField(write_only=True)
    user_id = serializers.IntegerField(source="id", read_only=True)
    
    class Meta:
        model = User
        fields = ["user_id", "username", "email", "password", "repeated_password", "type"]
        extra_kwargs = {
            "password": { "write_only": True },
            "email": { "required": True }
        }
        
    def validate_type(self, value):
        if value != "business" and value != "customer":
            raise serializers.ValidationError("type field can only be 'business' or 'customer'.")
        return value
            
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already in use.")
        return value
        
    def validate(self, data):
        if data["password"] != data["repeated_password"]:
            raise serializers.ValidationError({"error": "Passwords don't match!"})
        return data
    
    def create(self, validated_data):
        return User.objects.create_user(username=validated_data["username"], password=validated_data["password"], email=validated_data["email"])
    
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)
        
    def validate(self, data):
        user = authenticate(username=data["username"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Username or password is incorrect.")
        data["user"] = user
        return data      