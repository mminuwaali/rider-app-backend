from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("transaction", views.TransactionViewSet, "transaction")

urlpatterns = [
    path("verify/<str:refrence>/", views.VerifyTransactionAPIView.as_view(), name="verify"),
    path("withdraw/", views.WithdrawAPIView.as_view(), name="withdraw"),
    path("", views.WalletAPIView.as_view(), name="wallet"),
    path("", include(router.urls)),
]
