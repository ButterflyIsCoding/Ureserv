from celery import shared_task
from .models import Reservation
from django.utils.timezone import now

@shared_task
def auto_delete_expired_reservations():
    now_date = now().date()
    now_time = now().time()
    expired_reservations = Reservation.objects.filter(
        date__lt=now_date
    ) | Reservation.objects.filter(
        date=now_date,
        end_time__lt=now_time
    )
    count = expired_reservations.count()
    expired_reservations.delete()
    return f"{count} expired reservations deleted."
