from django.db.models import F
from . import models, serializers
from rest_framework.views import APIView
from rideapp.models import RiderLocation
from rest_framework_simplejwt import views
from rideapp.utils import calculate_distance
from django.contrib.auth import update_session_auth_hash
from rest_framework import status, viewsets, response, permissions, decorators


class SigninView(views.TokenObtainPairView):
    permission_classes = [permissions.AllowAny]


class VerifyTokenView(views.TokenVerifyView):
    permission_classes = [permissions.AllowAny]


class RefreshTokenView(views.TokenRefreshView):
    permission_classes = [permissions.AllowAny]

class AddressView(APIView):
    def get_serializer(self, *args, **kwargs):
        return serializers.AddressSerializer(*args, **kwargs)

    def get_queryset(self):
        return self.request.user.address_set.all()

    def get(self, request):
        queryset = self.get_queryset()

        serializer = serializers.AddressSerializer(queryset, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user

        serializer = self.get_serializer(data=request.data, context={"user":user})
        if serializer.is_valid():
            serializer.save()

            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def patch(self, request):
    #     user = request.user

    #     serializer = self.get_serializer(data=request.data, context={"user":user}, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()

    #         return response.Response(serializer.data, status=status.HTTP_200_OK)
    #     return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def patch(self, request):
    #     user = request.user

    #     serializer = self.get_serializer(user, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()

    #         return response.Response(serializer.data, status=status.HTTP_200_OK)
    #     return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SettingsApiView(APIView):
    def get_serializer(self, *args, **kwargs):
        return serializers.ClientSerializer(*args, **kwargs)

    def get_object(self,  *args, **kwargs):
        return


class SignupView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    def get_serializer(self, *args, **kwargs):
        return serializers.UserSerializer(*args, **kwargs)

    def get(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = request.user

        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RiderView(APIView):
    def get_serializer(self, *args, **kwargs):
        return serializers.RiderSerializer(*args, **kwargs)

    def get(self, request):
        user = request.user
        serializer = self.get_serializer(user.rider)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = request.user

        serializer = self.get_serializer(user.rider, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Initialize the serializer with the user and request data
        serializer = serializers.PasswordChangeSerializer(data=request.data, context={'user': request.user})

        if serializer.is_valid():
            # Set the new password
            new_password = serializer.validated_data['new_password']
            request.user.set_password(new_password)
            request.user.save()

            # Update the session to keep the user logged in
            update_session_auth_hash(request, request.user)

            return response.Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)