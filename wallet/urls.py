from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("transaction", views.TransactionViewSet, "transaction")

urlpatterns = [
    path("initialize-payment/", views.InitializePaymentAPIView.as_view(), name="initialize-payment"),
    path("verify/", views.VerifyTransactionAPIView.as_view(), name="verify"),
    path("withdraw/", views.WithdrawAPIView.as_view(), name="withdraw"),
    path("", views.WalletAPIView.as_view(), name="wallet"),
    path("", include(router.urls)),
]
