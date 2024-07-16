from rest_framework import permissions
from .models import Invigilator, Student

class IsInvigilator(permissions.BasePermission):
    """
    Custom permission to only allow access to invigilators.
    """

    def has_permission(self, request, view):
        return bool(request.user and Invigilator.objects.filter(user=request.user).exists())

class IsStudent(permissions.BasePermission):
    """
    Custom permission to only allow access to students.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and Student.objects.filter(user=request.user).exists())

class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow access to superusers (admins).
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)