# Generated by Django 5.0.4 on 2024-04-18 19:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terrains', '0003_remove_reservation_facture_facture_reservations'),
    ]

    operations = [
        migrations.AddField(
            model_name='terrain',
            name='administrateur',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='terrains.administrateur'),
        ),
    ]
