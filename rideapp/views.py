from . import models, serializers
from rest_framework import viewsets

class ScheduleViewSet(viewsets.ModelViewSet):
    filterset_fields = ["rider", "scheduled_date"]
    
    def get_queryset(self):
        return models.Schedule.objects.all()

    def get_serializer_class(self):
        return serializers.ScheduleSerializer

class BookingViewSet(viewsets.ModelViewSet):
    filterset_fields = ["client", "status"]
    
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
