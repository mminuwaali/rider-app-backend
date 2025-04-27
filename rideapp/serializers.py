from . import models
from rest_framework import serializers
from account.serializers import UserSerializer

class ScheduleSerializer(serializers.ModelSerializer):
    rider  = UserSerializer(read_only=True)

    class Meta:
        fields = "__all__"
        model = models.Schedule

    def validate(self, data):
        # Ensure start_time is earlier than end_time
        if data["start_time"] >= data["end_time"]:
            raise serializers.ValidationError("Start time must be earlier than end time.")
        return data

    def create(self, validated_data):
        validated_data["rider"] = self.context["request"].user
        return super().create(validated_data)

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.Booking


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.Request