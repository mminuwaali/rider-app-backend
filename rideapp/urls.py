from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("booking", views.BookingViewSet, "booking")
router.register("request", views.RequestViewSet, "request")
router.register("schedule", views.ScheduleViewSet, "schedule")


urlpatterns = [
    path("", include(router.urls)),
]
