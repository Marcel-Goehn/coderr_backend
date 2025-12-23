from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from auth_app.models import UserProfile


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
    
    
class ProfileSerializer(serializers.ModelSerializer):
    
    created_at = serializers.DateTimeField(source="user.date_joined", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")
    
    class Meta:
        model = UserProfile
        fields = ["user", "username", "first_name", "last_name", "file", "location", "tel", "description", "working_hours", "type", "email", "created_at"]
        read_only_fields = ["user", "type"]
        
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already in use.")
        return value
        
    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        user = instance.user
        user.first_name = user_data.get("first_name", user.first_name)
        user.last_name = user_data.get("last_name", user.last_name)
        instance.file = validated_data.get("file", instance.file)
        instance.location = validated_data.get("location", instance.location)
        instance.tel = validated_data.get("tel", instance.tel)
        instance.description = validated_data.get("description", instance.description)
        instance.working_hours = validated_data.get("workin_hours", instance.working_hours)
        user.email = user_data.get("email", user.email)
        user.save()
        instance.save()
        return instance
    
    
class BusinessProfileSerializer(serializers.ModelSerializer):
    
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ["user", "username", "first_name", "last_name", "file", "location", "tel", "description", "working_hours", "type"]
        read_only_fields = ["user", "file", "location", "tel", "description", "working_hours", "type"]
        
        
class CustomerProfileSerializer(serializers.ModelSerializer):
    
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ["user", "username", "first_name", "last_name", "file", "type"]
        read_only_fields = ["user", "file", "type"]
        