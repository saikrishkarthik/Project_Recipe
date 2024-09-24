from rest_framework import serializers
from user_auth.models import LoginUser
from django.contrib.auth import authenticate
import re

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginUser
        fields = ['username', 'password', 'email', 'token', 'is_active']


    # Validate the username
    def validate_username(self, value):
        if LoginUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        
        return value


    # Validate the email
    def validate_email(self, value):
        if LoginUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise serializers.ValidationError("Please enter a valid email address.")
        
        return value


    # Validate the password (custom validation can be added)
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        
        return value


    def validate(self, data):   # validation for email if its blank
        if 'email' not in data or not data['email']:
            raise serializers.ValidationError("Please enter your email address.")
        return data