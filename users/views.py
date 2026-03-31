from django.contrib.auth import get_user_model, authenticate
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
import threading

from .serializers import UserSerializer
from university_portal.utils.email import send_mail

User = get_user_model()


class Register(APIView):
    """Register a new user."""
    permission_classes = [AllowAny]
    def post(self, request):
        """Handle user registration."""
        try:
            serializer = UserSerializer(data=request.data)
            
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            data = serializer.validated_data
            print(f"Validated data: {data}")
            from django.db import transaction

            try:
                if User.objects.filter(email=data['email']).exists():
                    return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
                with transaction.atomic():
                    
                    raw_pass = get_random_string(length=10)
                    
                    if raw_pass == user.username:
                        raw_pass = get_random_string(length=10)
                
                    user = User(
                        email=data['email'],
                        first_name=data['first_name'],
                        last_name=data['last_name'],
                        role=str(data['role']).lower(),
                    )

                    user.set_password(raw_pass)
                    user.save()
                    
                    def send_email():
                        message = f"""
                            Welcome to University Portal!\n\nYour account has been created.\n
                            Username: {user.username}\nPassword: {raw_pass}\n\n
                        """
                        
                        send_mail(
                            subject="Welcome to University Portal",
                            message=message,
                            recipient_list=[user.email]
                        )
                    threading.Thread(target=send_email).start()
            
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'user': UserSerializer(user).data}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    
class Login(APIView):
    """User login view."""
    permission_classes = [AllowAny]
    def post(self, request):
        """Handle user login."""
        print("start login")
        try:
            print(f"request data: {request.data}")
            username = request.data.get('username')
            password = request.data.get('password')
            
            print(f"Login attempt with username: {username}\n{password}")  # Debugging statement
            if not username or not password:
                return Response({'error': 'Wrong Credentials'}, status=status.HTTP_400_BAD_REQUEST)
            
            user = authenticate(username=username, password=password)
            print(f"Authenticated user: {user}")
            
            if user is not None:
                refresh = RefreshToken.for_user(user)
                response = {'refresh': str(refresh), 'access': str(refresh.access_token), 'user': UserSerializer(user).data}
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Wrong Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)