from . import models
from django.contrib import admin

@admin.register(models.Wallet)
class WalletAdmin(admin.ModelAdmin):
    search_fields = ["user__username"]
    list_display = ["user", "amount", "created_at", "updated_at"]

@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    search_fields = ["reference"]
    list_filter = ["wallet", "type"]
    list_display = ["reference", "wallet", "type", "amount","created_at", "updated_at"]

    def type(self, obj):
        return obj.type.name.title()


@admin.register(models.TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name", "created_at", "updated_at"]
