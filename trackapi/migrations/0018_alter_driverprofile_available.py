# Generated by Django 4.0.6 on 2022-07-25 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trackapi', '0017_remove_route_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverprofile',
            name='available',
            field=models.BooleanField(default=True),
        ),
    ]
