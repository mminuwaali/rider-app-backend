# Generated by Django 5.1.7 on 2025-04-26 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_rider_price_per_km_rider_service_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='rider',
            name='capacity',
            field=models.IntegerField(default=0),
        ),
    ]
