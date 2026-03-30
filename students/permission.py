"""
Permission classes for the user roles
"""
from rest_framework.permissions import BasePermission

class IsStudent(BasePermission):
    """Permission class for students."""
    def has_permission(self, request, view):
        """Check if the user is a student."""
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'role') and
            getattr(request.user.role, 'name', '').lower() == 'student'
        )

class IsTeacher(BasePermission):
    """Permission class for teachers."""
    def has_permission(self, request, view):
        """Check if the user is a teacher."""
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'role') and
            getattr(request.user.role, 'name', '').lower() == 'teacher'
        )