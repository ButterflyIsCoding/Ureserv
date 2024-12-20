from django.db import models
from django.conf import settings

class Hall(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    equipments = models.TextField(max_length=100)

    def __str__(self):
        return self.name

class Reservation(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=100)
    professor_email = models.EmailField()
    delegate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')
    level = models.CharField(max_length=50)  # Assuming level is a string field
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()
    is_validated = models.BooleanField(default=False)
    validation_token = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Automatically set the level based on the delegate
        if self.delegate:
            self.level = self.delegate.niveau
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.course_name} - {self.date} ({self.start_time} to {self.end_time})"

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
