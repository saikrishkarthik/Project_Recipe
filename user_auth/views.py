
import uuid
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate, login
from user_auth.models import LoginUser
from user_auth.serializers import UserSerializer
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import serializers

logger = logging.getLogger(__name__)


class UserCreateView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    
    def post(self, request):
        """
        API - /auth/register/
        sample request:
            {
                "username" : "Vinayak",
                "password": "Vinayak@786",
                "email" : "Vinayak@gmail.com"
            }
          
        sample response:
            {
                "status": "success",
                "message": "User registered successfully. Please login."
            }
        """
        try:
            data = request.data
            serializer = UserSerializer(data=data)

            # Validate the user data
            if serializer.is_valid():
                validated_data = serializer.validated_data

                # Create user manually in the view
                LoginUser.objects.create(username=validated_data['username'], email=validated_data['email'],
                    password=validated_data['password'])

                return Response({'status': 'success', 'message': 'User registered successfully. Please login.'}, status=status.HTTP_201_CREATED)

            return Response({'status': 'fail', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception(f'Exception {e}')
            return Response({'status': 'fail', 'message': 'Something went wrong, try again later.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        """
        API - /auth/login/
        sample request:
            {
             "username" : "Vinayak",
             "password": "Vinayak@786"
            }
          
        sample response:
            {
                "message": "Login successful",
                "user": ["Vinayak"],
                "token": "86cad706-0375-4c92-8ea7-5f0cd40bca97"
            }
        """
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            
            user = LoginUser.objects.filter(username=username, password=password)
            
            if user:
                token = str(uuid.uuid4())
                user.update(token = token)  # Update the token field
                
                # Return a success response
                return Response({"message": "Login successful", "user":user.values_list('username', flat=True),"token": token}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception(f'Exception {e}')
            return Response({'status': 'fail', 'message': 'Something went wrong, try again later.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        





class TokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return None
        try:
            user_token = LoginUser.objects.get(token=token)
            return (user_token, None)
        except LoginUser.DoesNotExist:
            raise AuthenticationFailed('Invalid token')