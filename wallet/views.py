from . import models, serializers
from rest_framework import views, viewsets, response

class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    def get_serializer_class(self):
        return serializers.TransactionSerializer

    def get_queryset(self):
        return models.Transaction.objects.filter(wallet__user=self.request.user)

class WalletAPIView(views.APIView):
    def get(self, request, *args, **kwargs):
        wallet = models.Wallet.objects.get(user=request.user)
        serializer = serializers.WalletSerializer(wallet)

        return response.Response(serializer.data, status=200)


class VerifyTransactionAPIView(views.APIView):
    def post(self, request, *args, **kwargs):
        ...

        
class WithdrawAPIView(views.APIView):
    def post(self, request, *args, **kwargs):
        ...

        
