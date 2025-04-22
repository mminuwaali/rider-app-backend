from . import models, serializers
from rest_framework.views import APIView
from rest_framework_simplejwt import views
from rest_framework import status, viewsets, response, permissions


class SigninView(views.TokenObtainPairView):
    permission_classes = [permissions.AllowAny]


class VerifyTokenView(views.TokenVerifyView):
    permission_classes = [permissions.AllowAny]


class RefreshTokenView(views.TokenRefreshView):
    permission_classes = [permissions.AllowAny]

class SettingsApiView(APIView):
    def get_serializer(self, *args, **kwargs):
        return serializers.ClientSerializer

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
