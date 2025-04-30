from . import models
from django.db import transaction
from django.db.models import signals
from django.dispatch import receiver
from django.contrib.auth import get_user_model

@receiver(signals.post_save, sender=get_user_model())
def create_user_wallet(sender, instance,created, *args, **kwargs):
    if created:
        try:
            models.Wallet.objects.create(user=instance)
        except Exception as e:
            print("Failed to create user wallet", e)