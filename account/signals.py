from . import models
from django.core import mail

# from django.urls import reverse
from django.dispatch import receiver

from django.db.models import signals
from django.template.loader import render_to_string

from django_rest_passwordreset import models
from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, *args, **kwargs):
    reset_password_token = kwargs.get("reset_password_token")
    user = reset_password_token.user

    user.email_user(
        "Password Reset Token",
        html_message=render_to_string(
            "account/password/reset_password_token.html",
            {"user": user, "token": reset_password_token},
        ),
    )

@receiver(signals.post_save, sender=models.User)
def create_user_settings(sender, instance, created, *args, **kwargs):
    if created:
        try:
            if instance.role == "rider":
            models.Rider.object.create(user=user)

            if instance.role == "client":
                models.Client.object.create(user=user)
        except Exception as e:
            print("Failed to create user settings", e)