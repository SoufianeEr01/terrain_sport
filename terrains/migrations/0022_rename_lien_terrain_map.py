# Generated by Django 5.0.3 on 2024-05-17 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('terrains', '0021_remove_terrain_latitude_remove_terrain_longitude_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='terrain',
            old_name='lien',
            new_name='map',
        ),
    ]
