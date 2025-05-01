from . import models
from uuid import uuid4
from django.db import transaction
from django.dispatch import receiver
from django.db.models import signals
from wallet.models import Transaction, TransactionType

@receiver(signals.post_save, sender=models.Request)
def deduct_price_from_users_after_ride(sender, instance, created,*args, **kwargs):
    if not created and instance.status == "completed":
        try:
            with transaction.atomic():
                rider = instance.rider
                client = instance.client

                rider.wallet.amount += instance.price
                client.wallet.amount -= instance.price

                rider.wallet.save()
                client.wallet.save()

                trans_type, _ = TransactionType.objects.get_or_create(name="ride")

                Transaction.objects.create(reference="Paid for ride",type=trans_type, wallet=client.wallet)
                Transaction.objects.create(reference="Amount for recent ride",type=trans_type, wallet=rider.wallet)
        except Exception as e:
            print("Failed to create and deduct price", e)