# Generated by Django 5.1.3 on 2024-11-27 20:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservationapp', '0002_reservation_school'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='school',
        ),
    ]
