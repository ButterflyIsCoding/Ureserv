from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.core.mail import send_mail
from .models import Hall, Reservation, Notification
from .serializer import HallSerializer, ReservationSerializer, NotificationSerializer
from django.conf import settings
import uuid
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.utils.timezone import now
from .util import send_in_app_notification
from datetime import datetime, timedelta
from rest_framework import permissions, status


# PermissionMakeReservation: Check if the user has the 'delegue' role to make reservations
class PermissionMakeReservation(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        # Only users with the 'delegue' role are allowed to make reservations
        if user.role != 'delegue':
            return Response({"error": "Only delegates can make reservations."}, status=status.HTTP_403_FORBIDDEN)
        return Response({"message": "Permission granted. You can proceed."})


# ResearchDate: Get available halls for a specific date
class ResearchDate(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, date):
        try:
            # Parse the date from the URL
            date = datetime.strptime(date, "%Y-%m-%d").date()
            # Get reservations for the specified date
            reservations = Reservation.objects.filter(date=date)
            reserved_halls = reservations.values_list('hall_id', 'start_time', 'end_time')

            # Create a dictionary to track reserved times for each hall
            hall_reservations = {}
            for hall_id, start_time, end_time in reserved_halls:
                if hall_id not in hall_reservations:
                    hall_reservations[hall_id] = []
                hall_reservations[hall_id].append((start_time, end_time))

            free_halls = []
            for hall in Hall.objects.all():
                if hall.id in hall_reservations:
                    # Get reserved time slots for this hall
                    reserved_slots = hall_reservations[hall.id]
                    available_hours = self.get_available_hours(reserved_slots, date)
                else:
                    available_hours = ["Available all day"]  # No reservations for this hall

                free_halls.append({
                    "hall": HallSerializer(hall).data,
                    "hours": available_hours
                })

            return Response(free_halls, status=status.HTTP_200_OK)

        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

    def get_available_hours(self, reserved_slots, date):
        # Assuming the hall operates from 7 AM to 11 PM
        start_of_day = datetime.combine(date, datetime.min.time()).replace(hour=7)
        end_of_day = datetime.combine(date, datetime.min.time()).replace(hour=23)

        available_hours = []
        last_end_time = start_of_day

        # Sort the reserved slots by start time
        reserved_slots.sort(key=lambda x: x[0])

        for start_time, end_time in reserved_slots:
            # Ensure start_time and end_time are datetime objects
            start_time = datetime.combine(date, start_time)
            end_time = datetime.combine(date, end_time)
  
            if last_end_time < start_time:
                available_hours.append(f"{last_end_time.strftime('%H:%M')} - {start_time.strftime('%H:%M')}")
            last_end_time = max(last_end_time, end_time)

        if last_end_time < end_of_day:
            available_hours.append(f"{last_end_time.strftime('%H:%M')} - {end_of_day.strftime('%H:%M')}")

        return available_hours


# MakeReservation: Create a reservation for a delegate, including validation
class MakeReservation(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        user = request.user

        # Validate that the user is a delegate
        if user.role != 'delegue':
            return Response({"error": "Only delegates can make reservations."}, status=status.HTTP_403_FORBIDDEN)

        # Validate the date and time format
        try:
            reservation_date = datetime.strptime(data.get('date'), "%Y-%m-%d").date()
            start_time = datetime.strptime(data.get('start_time'), "%H:%M:%S").time()
            end_time = datetime.strptime(data.get('end_time'), "%H:%M:%S").time()
        except ValueError:
            return Response({"error": "Invalid date or time format. Use 'YYYY-MM-DD' for date and 'HH:MM:SS' for time."}, status=status.HTTP_400_BAD_REQUEST)

        current_time = now()

        # Check if the reservation date is in the past
        if reservation_date < current_time.date():
            return Response({"error": "Cannot make a reservation for a past date."}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure the reservation start time is not in the past for the current day
        if reservation_date == current_time.date() and start_time <= current_time.time():
            return Response({"error": "Cannot make a reservation for a past time on the same day."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate that the end time is after the start time
        if end_time <= start_time:
            return Response({"error": "End time must be after the start time."}, status=status.HTTP_400_BAD_REQUEST)

        # Check for overlapping reservations for the same hall at the requested time
        hall = get_object_or_404(Hall, id=data.get('hall_id'))
        overlapping_reservations = Reservation.objects.filter(
            hall=hall,
            date=reservation_date
        ).filter(
            start_time__lt=end_time,  # New reservation overlaps with an existing one’s end time
            end_time__gt=start_time   # New reservation overlaps with an existing one’s start time
        )

        if overlapping_reservations.exists():
            return Response({"error": "This time slot is already reserved for the selected hall."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the reservation and send email to professor for validation
        token = str(uuid.uuid4())
        reservation = Reservation.objects.create(
            hall=hall,
            course_name=data.get('course_name'),
            professor_email=data.get('professor_email'),
            delegate=user,
            start_time=start_time,
            end_time=end_time,
            date=reservation_date,
            validation_token=token
        )

        # Send the validation email to the professor
        validation_link = f"{settings.FRONTEND_URL}/validate-reservation/{token}"
        send_mail(
            subject="Validate Reservation",
            message=f"Click the following link to validate the reservation: {validation_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[reservation.professor_email]
        )

        # Send in-app notification to delegate
        send_in_app_notification(user, "Reservation Created", f"Your reservation for {reservation.course_name} on {reservation.date} has been created and is awaiting professor validation.")

        return Response({"reservation_id": reservation.id, "message": "Reservation created and validation email sent."}, status=status.HTTP_201_CREATED)


# ValidateReservation: Handle validation of reservations by the professor using a token
class ValidateReservation(APIView):
    def get(self, request, token):
        try:
            reservation = Reservation.objects.get(validation_token=token)
            reservation.is_validated = True
            reservation.validation_token = None
            reservation.save()

            # Send in-app notification to the delegate
            send_in_app_notification(reservation.delegate, "Reservation Validated", f"Your reservation for {reservation.course_name} on {reservation.date} has been validated.")

            return Response({"message": "Reservation validated successfully."}, status=status.HTTP_200_OK)
        except Reservation.DoesNotExist:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_404_NOT_FOUND)


# GetReservationsByLevel: Retrieve reservations for users of the same level
class GetReservationsByLevel(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        user_level = user.niveau  # Assuming 'niveau' is the field for the user's level

        if not user_level:
            return Response({"error": "User level not found."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch reservations for the same level
        reservations = Reservation.objects.filter(level=user_level)

        if not reservations.exists():
            return Response({"message": "No reservations found for this level."}, status=status.HTTP_404_NOT_FOUND)

        # Extract only the required fields
        reservations_data = [
            {
                "hall_name": reservation.hall.name,
                "course_name": reservation.course_name,
                "start_time": reservation.start_time,
                "end_time": reservation.end_time,
                "date": reservation.date
            }
            for reservation in reservations
        ]

        return Response({"reservations": reservations_data}, status=status.HTTP_200_OK)


# GetNotificationsByLevel: Retrieve notifications for users of the same level
class GetNotificationsByLevel(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        user_level = user.niveau  # Assuming 'niveau' is the field for the user's level

        if not user_level:
            return Response({"error": "User level not found."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch notifications for the same level
        notifications = Notification.objects.filter(user__niveau=user_level)

        if not notifications.exists():
            return Response({"message": "No notifications found for this level."}, status=status.HTTP_404_NOT_FOUND)

        # Extract only the required fields
        notifications_data = [
            {
                "title": notification.title,
                "message": notification.message,
                "created_at": notification.created_at
            }
            for notification in notifications
        ]

        return Response({"notifications": notifications_data}, status=status.HTTP_200_OK)


# InfoReservation: Get detailed information about a specific reservation by ID
class InfoReservation(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, reservation_id):
        reservation = get_object_or_404(Reservation, id=reservation_id)
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data, status=status.HTTP_200_OK)


class InfoHall(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, hall_name):
        hall = get_object_or_404(Hall, name=hall_name)
        serializer = HallSerializer(hall)
        return Response(serializer.data, status=status.HTTP_200_OK)




# Profile: Get the profile information of the currently authenticated user
class Profile(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        profile_info = {
            "id": user.id,
            "email": user.email,
            "username": user.nom,
            "role": user.role,
            "level": user.niveau
        }
        return Response(profile_info, status=status.HTTP_200_OK)


# PotentialReservationsToCancel: Get reservations that may potentially be cancelled by the user or admin
class PotentialReservationsToCancel(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, date=None):
        user = request.user
        if user.role == 'delegue':
            reservations = Reservation.objects.filter(delegate=user)
        elif user.role == 'administrateur' and date:
            reservations = Reservation.objects.filter(date=date)
        else:
            return Response({"error": "Invalid role or missing date."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# CancelReservation: Cancel a specific reservation and notify the delegate or professor
class CancelReservation(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, reservation_id):
        user = request.user
        reservation = get_object_or_404(Reservation, id=reservation_id)

        if user.role == 'delegue' and reservation.delegate == user:
            reservation.delete()

            # In-App notification to the delegate
            send_in_app_notification(reservation.delegate, "Reservation Cancelled", f"Your reservation for {reservation.course_name} on {reservation.date} was cancelled.")

        elif user.role == 'administrateur':
            reservation.delete()

            # In-App notification to the delegate
            send_in_app_notification(reservation.delegate, "Reservation Cancelled by Admin", f"Your reservation for {reservation.course_name} on {reservation.date} was cancelled by the administration.")

            # Send email to professor
            send_mail(
                subject="Reservation Cancelled",
                message=f"The reservation for {reservation.course_name} was cancelled by the administration.",
                from_email="admin@example.com",
                recipient_list=[reservation.professor_email]
            )
        else:
            return Response({"error": "Unauthorized action."}, status=status.HTTP_403_FORBIDDEN)

        return Response({"message": "Reservation cancelled successfully."}, status=status.HTTP_200_OK)


# CancelAllReservations: Admin function to cancel all reservations for a specific date
class CancelAllReservations(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, date):
        user = request.user
        if user.role != 'administrateur':
            return Response({"error": "Unauthorized action."}, status=status.HTTP_403_FORBIDDEN)

        reservations = Reservation.objects.filter(date=date)
        for reservation in reservations:
            Notification.objects.create(
                user=reservation.delegate,
                title="Reservation Cancelled",
                message=f"All reservations on {date} were cancelled by the administration."
            )
        reservations.delete()
        return Response({"message": "All reservations cancelled successfully."}, status=status.HTTP_200_OK)


# AutoDeleteExpiredReservations: Automatically delete expired reservations from the system
class AutoDeleteExpiredReservations(APIView):
    """
    Deletes expired reservations from the database.
    Expired reservations are those where the reservation date and time have passed,
    including those that were not validated.
    """
    def delete(self, request):
        current_date = now().date()
        current_time = now().time()

        # Filter expired reservations (past date or expired time)
        expired_reservations = Reservation.objects.filter(
            date__lt=current_date  # Reservations before today
        ) | Reservation.objects.filter(
            date=current_date,  # Reservations today but with expired end time
            end_time__lt=current_time
        )

        # Include unvalidated reservations
        expired_reservations = expired_reservations.filter(is_validated=False) | expired_reservations.filter(
            validation_token__isnull=False
        )

        expired_reservations.delete()

        return Response({"message": "Expired reservations deleted successfully."}, status=status.HTTP_200_OK)

##Return all halls
class ResearchHalls(APIView):

    def get(self, request):
        halls = []
        for hall in Hall.objects.all():
            halls.append({
                "hall": HallSerializer(hall).data
            })

        return Response(halls, status=status.HTTP_200_OK)