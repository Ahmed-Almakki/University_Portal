"""
Serializer for User model in students app.
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""
    role = serializers.StringRelatedField()

    class Meta:
        """Meta class for the UserSerializer."""
        model = User
        fields = ['id', 'admission_year', 'student_id', 'role', 'username', 'email']