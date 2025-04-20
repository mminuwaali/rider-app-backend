from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLES = [
        ("rider", "r"),
        ("client", "c"),
    ]

    profile = models.ImageField(upload_to="profiles", null=True, blank=True)
    role = models.CharField(null=True,blank=True, choices=ROLES, max_length=20)


class Rider(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)


class Client(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)