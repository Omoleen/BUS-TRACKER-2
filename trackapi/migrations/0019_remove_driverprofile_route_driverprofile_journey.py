# Generated by Django 4.0.6 on 2022-07-25 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trackapi', '0018_alter_driverprofile_available'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='driverprofile',
            name='route',
        ),
        migrations.AddField(
            model_name='driverprofile',
            name='journey',
            field=models.ManyToManyField(related_name='route', to='trackapi.route'),
        ),
    ]
