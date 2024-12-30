from .models import Notification
from django.utils import timezone

def send_in_app_notification(user, title, message):
    """
    Sends an in-app notification to a specific user.

    Args:
    - user: The User object to send the notification to.
    - title: The title of the notification.
    - message: The message/content of the notification.
    """
    # Create and save the notification
    Notification.objects.create(
        user=user,
        title=title,
        message=message,
        created_at=timezone.now(),
        is_read=False  # Notification is unread by default
    )