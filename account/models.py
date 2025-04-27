from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLES = [
        ("rider", "r"),
        ("client", "c"),
    ]
    GENDERS = [
        ("male", "m"),
        ("female", "f"),
    ]

    profile = models.ImageField(upload_to="profiles", null=True, blank=True)
    role = models.CharField(null=True,blank=True, choices=ROLES, max_length=20)
    gender = models.CharField(null=True,blank=True, choices=GENDERS, max_length=20)


class Rider(models.Model):
    SERVICE_CHOICES = [
        ('both', 'b'),
        ('rides', 'r'),
        ('packages', 'p'),
    ]

    capacity = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    price_per_km = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    service_type = models.CharField(null=True,blank=True, choices=SERVICE_CHOICES, max_length=20)


class Client(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)