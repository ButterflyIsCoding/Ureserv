from rest_framework.permissions import BasePermission
from .models import CustomUser

class IsAdministrator(BasePermission):
    """
    Permission pour vérifier si l'utilisateur authentifié est un administrateur.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'administrateur'
