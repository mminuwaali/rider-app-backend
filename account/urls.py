from . import views
from django.urls import path, include
from django_rest_passwordreset import urls

urlpatterns = [
    path("signin/", views.SigninView.as_view(), name="signin"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("password/", include(urls, namespace="password_reset")),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("verify/", views.VerifyTokenView.as_view(), name="verify"),
    path("refresh/", views.RefreshTokenView.as_view(), name="refresh"),
]
