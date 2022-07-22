# Generated by Django 3.2.13 on 2022-07-20 22:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trackapi', '0002_driver_passenger'),
    ]

    operations = [
        migrations.CreateModel(
            name='PassengerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passenger_id', models.IntegerField(blank=True)),
                ('payment_method', models.CharField(blank=True, choices=[('DEBIT', 'Debit'), ('TRANSFER', 'Transfer')], max_length=128)),
                ('in_ride', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='trackapi.passenger')),
            ],
        ),
        migrations.CreateModel(
            name='DriverProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='trackapi.driver')),
            ],
        ),
    ]