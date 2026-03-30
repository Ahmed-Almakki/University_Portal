from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
import threading

from .serializers import UserSerializer


User = get_user_model()


@api_view(['POST'])
def Register(request):
    """Register a new user."""
    try:
        serializer = UserSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        
        try:
            raw_pass = User.objects.make_random_password()
        
            user = User.objects.create_user(
                student_id=data['student_id'],
                admission_year=data['admission_year'],
                role=data['role'],
            )

            user.set_password(raw_pass)
            user.save()
            
            def send_email():
                from .utils.email import send_mail


                message = f"""
                    Welcome to University Portal!\n\nYour account has been created.\n
                    Username: {user.username}\nPassword: {raw_pass}\n\n
                    Please log in and change your password as soon as possible.
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


@api_view(['POST'])
def Login(request):
    """User login view."""
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user': UserSerializer(user).data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)