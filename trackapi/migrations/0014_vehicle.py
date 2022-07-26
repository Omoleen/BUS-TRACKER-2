# Generated by Django 4.0.6 on 2022-07-22 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trackapi', '0013_passengerrides_payment_method_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tracking_id', models.CharField(max_length=128)),
                ('plate_number', models.CharField(max_length=128)),
                ('is_active', models.BooleanField(default=True)),
                ('driver', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='trackapi.driver')),
            ],
        ),
    ]
