from django.urls import path
<<<<<<< HEAD
from .views import RegisterView, ApproveDelegateView, LoginView, PendingDelegatesView

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),  # Inscription d'un utilisateur
    path('approve-delegate/', ApproveDelegateView.as_view(), name='approve-delegate'),  # Approbat° des délégués (Admin seulement)
    path('login/', LoginView.as_view(), name='login'),  # Connexion utilisateur
    path('pending-delegates/', PendingDelegatesView.as_view(), name='pending-delegates'),
=======
from .views import *

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),  # Ajoutez .as_view()
    path('approve-delegate/<int:user_id>/', ApproveDelegateView.as_view(), name='approve-delegate'),  # Ajoutez .as_view()
    path('login/', LoginView.as_view(), name='login'),
>>>>>>> 346bbacefa667e29d78f773503ee09874ed8cf05
]
