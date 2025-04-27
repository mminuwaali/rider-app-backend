from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

User = get_user_model() 


class Schedule(models.Model):
    end_time = models.TimeField()
    start_time = models.TimeField()
    scheduled_date = models.DateField()
    routes = models.JSONField(default=list)
    rider = models.ForeignKey(User, models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    capacity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    price_per_km = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)]
    )


    def clean(self):
        # Ensure start_time is before end_time
        if self.start_time >= self.end_time:
            raise ValidationError("Start time must be before end time.")
        super().clean()


    class Meta:
        ordering = ["scheduled_date", "start_time"]
        unique_together = ["rider","start_time", "scheduled_date"]

    def __str__(self):
        return f"Rider: {self.rider.username}, Date: {self.scheduled_date}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    ]

    capacity = models.IntegerField(default=0)
    client = models.ForeignKey(User, models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    schedule = models.ForeignKey(Schedule, models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    ride_request = models.OneToOneField("Request", models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]


    def calculate_final_price(self):
        """Calculate the final charge for the client."""
        if self.schedule:
            # Use schedule's price_per_km
            return self.ride_request.calculate_price(self.schedule.price_per_km)
        return self.ride_request.calculate_price(self.ride_request.rider.rider.price_per_km)

    def __str__(self):
        if self.schedule:
            return f"Booking by {self.client} for Schedule {self.schedule.id}"


class Request(models.Model):
    REQUEST_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
        ("in_progress", "In Progress"),
    ]

    origin = models.JSONField() 
    destination = models.JSONField() 
    client = models.ForeignKey(User, models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    rider = models.ForeignKey(User, models.CASCADE, related_name="ride_requests")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=REQUEST_STATUS_CHOICES, default="pending")

    class Meta:
        ordering = ["-created_at"]

    def calculate_price(self, price_per_km):
        from geopy.distance import geodesic
        if self.origin and self.destination:
            origin_coords = (self.origin["latitude"], self.origin["longitde"])
            destination_coords = (self.destination["latitude"], self.destination["longitde"])
            distance_km = geodesic(origin_coords, destination_coords).km
            return round(distance_km * price_per_km, 2)
        return 0


    def __str__(self):
        return f"RideRequest by {self.client} from {self.origin['address']} to {self.destination['address']}"
