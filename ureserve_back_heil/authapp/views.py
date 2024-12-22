from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import UserSerializer
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from .email_utils import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import BasePermission
from .permissions import IsAdministrator
from .email_utils import send_delegue_approval_notification, send_etudiant_approval_notification
<<<<<<< HEAD

=======
# Create your views here.
>>>>>>> 346bbacefa667e29d78f773503ee09874ed8cf05


class RegisterView(APIView):
    """
    Vue pour enregistrer un utilisateur.
    - Étudiant : Enregistré immédiatement.
    - Délégué : Créé mais non approuvé.
    """
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            if user.role == 'etudiant':
                email_sent = send_etudiant_approval_notification(user)

                if not email_sent:
                    response_data['warning'] = "L'email de notification n'a pas pu être envoyé."##########

            if user.role == 'delegue':
                return Response({
                    'message': 'Délégué créé avec succès, en attente de validation par un administrateur.'
                }, status=status.HTTP_201_CREATED)
            return Response({'message': 'Utilisateur créé avec succès'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






<<<<<<< HEAD
class PendingDelegatesView(APIView):
    """
    Vue pour lister tous les délégués en attente d'approbation.
    Accessible uniquement aux administrateurs.
    """
    permission_classes = [IsAdministrator]

    def get(self, request):
        # Rechercher tous les délégués non approuvés
        pending_delegates = CustomUser.objects.filter(role='delegue', is_approved=False)
        serializer = UserSerializer(pending_delegates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)






=======
>>>>>>> 346bbacefa667e29d78f773503ee09874ed8cf05
class ApproveDelegateView(APIView):
    """
    Vue pour approuver un délégué.
    Accessible uniquement aux administrateurs.
    """
    permission_classes = [IsAdministrator]

<<<<<<< HEAD
    def post(self, request):
        # Récupérer l'ID de l'utilisateur depuis le corps de la requête
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'L\'identifiant user_id est requis.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Rechercher l'utilisateur correspondant
=======
    def post(self, request, user_id):
        try:
>>>>>>> 346bbacefa667e29d78f773503ee09874ed8cf05
            user = CustomUser.objects.get(id=user_id, role='delegue', is_approved=False)
            user.is_approved = True
            user.save()

<<<<<<< HEAD
            # Envoi de l'email (ne bloque pas en cas d'échec)
            email_sent = send_delegue_approval_notification(user)

            # Préparer la réponse
            response_data = {
                'message': 'Délégué approuvé avec succès.',
                'user': UserSerializer(user).data
            }
=======
            # Tentative d'envoi de l'email (ne bloque pas si échec)
            email_sent = send_delegue_approval_notification(user)

            response_data = {
                'message': 'Délégué approuvé avec succès.', 
                'user': UserSerializer(user).data
            }
            
>>>>>>> 346bbacefa667e29d78f773503ee09874ed8cf05
            if not email_sent:
                response_data['warning'] = "L'email de notification n'a pas pu être envoyé."

            return Response(response_data, status=status.HTTP_200_OK)
<<<<<<< HEAD
        
=======
            
>>>>>>> 346bbacefa667e29d78f773503ee09874ed8cf05
        except CustomUser.DoesNotExist:
            return Response({
                'error': 'Utilisateur non trouvé ou déjà approuvé.'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
<<<<<<< HEAD
                'error': f'Une erreur est survenue lors de l\'approbation : {str(e)}'
=======
                'error': f'Une erreur est survenue lors de l\'approbation: {str(e)}'
>>>>>>> 346bbacefa667e29d78f773503ee09874ed8cf05
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        try:
            user = CustomUser.objects.get(email=email)
            if check_password(password, user.password):
                if user.role == 'delegue' and not user.is_approved:
                    return Response({
                        'error': 'Compte délégué non approuvé'
                    }, status=status.HTTP_403_FORBIDDEN)
                
                # Génération des tokens
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserSerializer(user).data
                })
            return Response({
                'error': 'Mot de passe incorrect'
            }, status=status.HTTP_401_UNAUTHORIZED)
        except CustomUser.DoesNotExist:
            return Response({
                'error': 'Utilisateur non trouvé'
            }, status=status.HTTP_404_NOT_FOUND)
