from . import views
from django.urls import path, include
from django_rest_passwordreset import urls
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path("rider/", views.RiderView.as_view(), name="rider"),
    path("signin/", views.SigninView.as_view(), name="signin"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("password/", include(urls, namespace="password_reset")),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("verify/", views.VerifyTokenView.as_view(), name="verify"),
    path("refresh/", views.RefreshTokenView.as_view(), name="refresh"),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
]
