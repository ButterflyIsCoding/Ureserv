from django.urls import path
from .views import RegisterView, ApproveDelegateView, LoginView, PendingDelegatesView

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),  # Inscription d'un utilisateur
    path('approve-delegate/', ApproveDelegateView.as_view(), name='approve-delegate'),  # Approbat° des délégués (Admin seulement)
    path('login/', LoginView.as_view(), name='login'),  # Connexion utilisateur
    path('pending-delegates/', PendingDelegatesView.as_view(), name='pending-delegates'),
]
