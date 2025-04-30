from uuid import uuid4
from django.db import models, transaction
from django.contrib.auth import get_user_model

User = get_user_model()

class Wallet(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    total_deposit = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    total_withdrawn = models.DecimalField(default=0, decimal_places=2, max_digits=10)

    def deposit(self, amount:float, ref:str = uuid4(), **kwargs):
        with transaction.atomic():
            self.amount += amount
            self.total_deposit += amount

            trans_type, _ = TransactionType.objects.get_or_create(name="deposit")
            Transaction.objects.create(
                wallet=self,
                reference=ref,
                amount=amount,
                type=trans_type,
                status="completed",
                **kwargs
            )

            self.save()
    
    def withdraw(self, amount:float, ref:str = uuid4(), **kwargs):
        if self.amount < amount:
            raise ValueError("Insufficient funds for this withdrawal")
            
        with transaction.atomic():
            self.amount -= amount
            self.total_withdrawn += amount

            trans_type, _ = TransactionType.objects.get_or_create(name="withdrawal")
            Transaction.objects.create(
                wallet=self,
                amount=amount,
                reference=ref,
                type=trans_type,
                status="completed",
                **kwargs
            )

            self.save()

    def __str__(self):
        return f"{self.user.username}'s wallet"

class Transaction(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    wallet = models.ForeignKey(Wallet, models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.ForeignKey("TransactionType", models.PROTECT)
    status = models.CharField(max_length=20, default="pending")
    reference = models.CharField(max_length=200, default="", blank=True)
    amount = models.DecimalField(default=0, decimal_places=2, max_digits=10)

    def __str__(self):
        return f"{self.wallet.user.username}: {self.type.name} transaction of {self.amount}"

class TransactionType(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(unique=True, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name.title()