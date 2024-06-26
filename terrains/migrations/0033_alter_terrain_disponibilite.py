# Generated by Django 5.0.4 on 2024-05-22 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terrains', '0032_alter_reservation_montant_payer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='terrain',
            name='disponibilite',
            field=models.CharField(choices=[('Disponible', 'DISPONIBLE'), ('Non_disponible', 'NON_DISPONIBLE'), ('Reservé', 'RESERVE'), ('Maintenance', 'MAINTENANCE')], default='Disponible', max_length=20),
        ),
    ]
