from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),  # Ajoutez .as_view()
    path('approve-delegate/<int:user_id>/', ApproveDelegateView.as_view(), name='approve-delegate'),  # Ajoutez .as_view()
    path('login/', LoginView.as_view(), name='login'),
    path('pending-delegates/', PendingDelegatesView.as_view(), name='pending-delegates'),
    path('profile/', GetUserInfoView.as_view(), name='profile'),
]
