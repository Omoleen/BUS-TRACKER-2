# Generated by Django 4.0.6 on 2022-07-25 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trackapi', '0015_route_driverprofile_vehicle_driverprofile_route'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehicle',
            name='driver',
        ),
    ]
