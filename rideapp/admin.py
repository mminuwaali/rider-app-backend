from . import models
from django.contrib import admin


@admin.register(models.Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_filter = ["rider"]
    list_display = ["rider", "capacity", "price_per_km", "scheduled_date"]


@admin.register(models.Booking)
class BookingAdmin(admin.ModelAdmin):
    list_filter = ["client", "schedule", "status", "ride_request"]
    list_display = ["client", "status", "schedule", "ride_request"]


@admin.register(models.Request)
class RequestAdmin(admin.ModelAdmin):
    list_filter = ["status", "client", "rider"]
    list_display = ["status", "client", "rider"]
    search_fields = ["origin", "destination"]
