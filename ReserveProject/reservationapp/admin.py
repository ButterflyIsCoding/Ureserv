from django.contrib import admin
from .models import Hall, Reservation, Notification

admin.site.register(Hall)
admin.site.register(Reservation)
admin.site.register(Notification)
