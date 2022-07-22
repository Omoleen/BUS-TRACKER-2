# Generated by Django 3.2.13 on 2022-07-20 23:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trackapi', '0004_remove_passengerprofile_passenger_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='driverprofile',
            name='available',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='driverprofile',
            name='current_location',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='driverprofile',
            name='destination',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='driverprofile',
            name='in_trip',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='driverprofile',
            name='verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='driverprofile',
            name='verifyID',
            field=models.BinaryField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='PassengerRides',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(auto_now=True)),
                ('start_location', models.TextField()),
                ('destination', models.TextField()),
                ('Price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trackapi.passenger')),
            ],
        ),
        migrations.CreateModel(
            name='DriverRides',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(auto_now=True)),
                ('start_location', models.TextField()),
                ('destination', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trackapi.driver')),
            ],
        ),
    ]
