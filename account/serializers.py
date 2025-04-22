from . import models
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(write_only=True, required=True)  # Role is required for input

    class Meta:
        model = models.User
        extra_kwargs = {
            "password": {"write_only": True},
        }
        fields = [
            "id",
            "role",
            "email",
            "gender",
            "profile",
            "password",
            "username",
            "last_name",
            "first_name",
        ]

    def create(self, validated_data):
        # Extract the role and validate
        role = validated_data.pop('role', None)
        if role not in ["rider", "client"]:
            raise serializers.ValidationError({"role": "Role must be 'rider' or 'client'."})

        # Create the user
        user = models.User.objects.create_user(**validated_data)

        # Create related model based on the role
        if role == "rider":
            models.Rider.objects.create(user=user)
        elif role == "client":
            models.Client.objects.create(user=user)

        return user

    def to_representation(self, instance):
        # Check for related models dynamically
        data = super().to_representation(instance)
        if hasattr(instance, "rider"):
            data["role"] = "rider"
        elif hasattr(instance, "client"):
            data["role"] = "client"
        else:
            data["role"] = None  # Handle edge case where neither relationship exists

        return data


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ["user"]
        model = models.Client

class RiderSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ["user"]
        model = models.Rider