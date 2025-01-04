from django.urls import path
from .views import (
    PermissionMakeReservation, ResearchDate, MakeReservation,
    ValidateReservation, GetReservationsByLevel, GetNotificationsByLevel, InfoReservation, Profile, PotentialReservationsToCancel,
    CancelReservation, CancelAllReservations, AutoDeleteExpiredReservations, InfoHall, ResearchHalls
)

urlpatterns = [
    path('permission/', PermissionMakeReservation.as_view(), name='permission-make-reservation'),
    path('research/<str:date>/', ResearchDate.as_view(), name='research-date'),
    path('make-reservation/', MakeReservation.as_view(), name='make-reservation'),
    path('validate-reservation/<str:token>/', ValidateReservation.as_view(), name='validate-reservation'),
    path('reservations-by-level/', GetReservationsByLevel.as_view(), name='reservations-by-level'),
    path('notifications-by-level/', GetNotificationsByLevel.as_view(), name='notifications-by-level'),
    path('info-reservation/<int:reservation_id>/', InfoReservation.as_view(), name='info-reservation'),
    path('info-hall/<str:hall_name>/', InfoHall.as_view(), name='info-hall'),
    path('profile/', Profile.as_view(), name='profile'),
    path('potential-reservations-to-cancel/<str:date>/', PotentialReservationsToCancel.as_view(), name='potential-reservations-to-cancel'),
    path('cancel-reservation/<int:reservation_id>/', CancelReservation.as_view(), name='cancel-reservation'),
    path('cancel-all-reservations/<str:date>/', CancelAllReservations.as_view(), name='cancel-all-reservations'),
    path('auto-delete-expired-reservations/', AutoDeleteExpiredReservations.as_view(), name='auto-delete-expired-reservations'),
    path('research-hall/', ResearchHalls.as_view(), name='research-hall'),
]
