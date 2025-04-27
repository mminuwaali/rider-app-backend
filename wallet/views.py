from . import utils, models, serializers
from rest_framework import views, status, viewsets, response

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

        
class WithdrawAPIView(views.APIView):
    def post(self, request, *args, **kwargs):
        ...

        
class VerifyTransactionAPIView(views.APIView):
    def post(self, request, *args, **kwargs):
        reference = request.data.get("reference")
        if not reference:
            return response.Response(
                {"error": "Transaction reference is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verify transaction using utility function
        result = utils.verify_paystack_payment(reference)

        if not result["status"]:
            return response.Response(
                {"error": result["message"]},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Retrieve verified data
        paystack_data = result["data"]

        # Check if the user has a wallet
        try:
            wallet = models.Wallet.objects.get(user=request.user)
        except models.Wallet.DoesNotExist:
            return response.Response(
                {"error": "Wallet not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Get or create the transaction type
        transaction_type, _ = models.TransactionType.objects.get_or_create(name="Deposit")

        # Create a transaction record
        transaction = models.Transaction.objects.create(
            wallet=wallet,
            type=transaction_type,
            status="success" if paystack_data["status"] == "success" else "failed",
            reference=paystack_data["reference"],
            amount=paystack_data["amount"] / 100,  # Convert amount from kobo to naira
        )

        # Update wallet balance if successful
        if transaction.status == "success":
            wallet.amount += transaction.amount
            wallet.total_deposit += transaction.amount
            wallet.save()

        return response.Response(
            {
                "message": result["message"],
                "transaction_id": transaction.id,
                "transaction_status": transaction.status,
            },
            status=status.HTTP_200_OK
        )