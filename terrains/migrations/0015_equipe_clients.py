# Generated by Django 5.0.4 on 2024-04-19 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terrains', '0014_remove_equipe_clients'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipe',
            name='clients',
            field=models.ManyToManyField(related_name='equipes', to='terrains.client'),
        ),
    ]
