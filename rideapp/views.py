from django.db.models import Q
from . import models, serializers
from django.db import transaction
from django.utils.timezone import now
from .utils import calculate_distance
from rest_framework import decorators, response, viewsets


class ScheduleViewSet(viewsets.ModelViewSet):
    filterset_fields = ["rider", "scheduled_date"]

    def get_queryset(self):
        return models.Schedule.objects.all()

    def get_serializer_class(self):
        return serializers.ScheduleSerializer

    @decorators.action(["GET"], False, "get-schedule")
    def get_schedule(self, request, *args, **kwargs):
        """
        Start the first schedule for the current day, create requests for all
        bookings under the schedule, and attach the created requests to the bookings.
        """
        today = now().date()  # Get the current date

        # Get the first schedule for today that is not started yet
        schedule = models.Schedule.objects.filter(
            scheduled_date=today, is_started=False
        ).order_by("start_time").first()

        if not schedule:
            return response.Response(None, status=200)
        
        serializer = serializers.ScheduleSerializer(schedule)
        return response.Response(serializer.data, status=200)

    @decorators.action(["POST"], False, "start-schedule")
    def start_schedule(self, request, *args, **kwargs):
        """
        Start the first schedule for the current day, create requests for all
        bookings under the schedule, and attach the created requests to the bookings.
        """
        today = now().date()  # Get the current date

        # Get the first schedule for today that is not started yet
        schedule = models.Schedule.objects.filter(
            scheduled_date=today, is_started=False
        ).order_by("start_time").first()

        if not schedule:
            return response.Response(None, status=200)

        # Mark the schedule as started
        schedule.is_started = True
        schedule.save()

        # Fetch all bookings for the schedule that don't already have a request
        bookings = models.Booking.objects.filter(schedule=schedule, ride_request__isnull=True)

        if not bookings.exists():
            return response.Response(
                {"message": "No bookings available to start this schedule."},
                status=200
            )

        # Create requests for each booking and attach them to the bookings
        with transaction.atomic():
            for booking in bookings:
                ride_request = models.Request.objects.create(
                    destination=booking.destination,
                    capacity=booking.capacity,
                    origin=booking.origin,
                    client=booking.client,
                    rider=schedule.rider,
                    status="pending"
                )
                booking.ride_request = ride_request
                booking.save()

        return response.Response(
            {"message": f"Schedule for {today} started successfully. Requests have been created for all bookings."},
            status=200
        )

    @decorators.action(detail=False, methods=["GET"], url_path="closest-schedules")
    def closest_schedules(self, request):
        """Calculate distances and return the first 10 closest schedules."""
        latitude = float(request.query_params.get("latitude"))
        longitude = float(request.query_params.get("longitude"))

        if latitude is None or longitude is None:
            return response.Response({"error": "latitude and longitude are required parameters"}, status=400)

        target_point = {"latitude": latitude, "longitude": longitude}

        schedules = self.get_queryset()
        results = []

        for schedule in schedules:
            for route in schedule.routes:
                distance = calculate_distance(target_point, route)
                results.append({"schedule": schedule, "distance": distance})

        # Sort by distance and get the top 10 closest schedules
        sorted_results = sorted(results, key=lambda x: x["distance"])[:10]

        # Serialize the schedules
        serialized_data = [
            {
                "schedule": serializers.ScheduleSerializer(result["schedule"]).data,
                "distance": result["distance"]
            }
            for result in sorted_results
        ]

        print(serialized_data)
        return response.Response(serialized_data)

class BookingViewSet(viewsets.ModelViewSet):
    filterset_fields = ["client", "status", "schedule"]

    def get_queryset(self):
        return models.Booking.objects.all()

    def get_serializer_class(self):
        return serializers.BookingSerializer


class RequestViewSet(viewsets.ModelViewSet):
    filterset_fields = ["client", "status"]

    def get_queryset(self):
        return models.Request.objects.all()

    def get_serializer_class(self):
        return serializers.RequestSerializer

    @decorators.action(["GET"], False, "my-ride")
    def get_my_ride(self, *args, **kwargs):
        user = self.request.user
        ride = models.Request.objects.filter(Q(client=user)| Q(rider=user))
        ride = ride.exclude(status__in=["completed", "cancelled"]).first()

        if not ride:
            return response.Response(None, 200)

        serializer = serializers.RequestSerializer(ride)
        return response.Response(serializer.data, 200)
