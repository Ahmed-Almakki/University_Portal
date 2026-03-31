"""
Permission classes for the user roles
"""
from rest_framework.permissions import BasePermission


class IsStudent(BasePermission):
    """Allows access only to students."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'student')

class IsTeacher(BasePermission):
    """Allows access only to teachers."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'teacher')

class IsAdmin(BasePermission):
    """Allows access only to admins."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'admin')