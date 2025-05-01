from . import models
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        # Check if the old password is correct
        user = self.context.get('user')
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate(self, data):
        # Ensure that new_password and confirm_password match
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("New password and confirm password do not match.")
        
        # Validate new password strength
        try:
            password_validation.validate_password(data['new_password'], self.context.get('user'))
        except ValidationError as e:
            raise serializers.ValidationError({'new_password': e.messages})
        
        return data

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
    # user = serializers.PrimaryKeySerializer(write_only=True)
    
    class Meta:
        exclude = ["user"]
        model = models.Client

class RiderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        fields = "__all__"
        model = models.Rider

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['user']
        model = models.Address

    def create(self, validated_data):
        validated_data['user'] = self.context.get("user")
        return models.Address.objects.create(**validated_data)