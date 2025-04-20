from . import models
from rest_framework import serializers

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ["user"]
        model = models.Wallet

class TransactionSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source="type.name")
    
    class Meta:
        exclude = ["wallet"]
        model = models.Transaction
