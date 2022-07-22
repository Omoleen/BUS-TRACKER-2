# Generated by Django 3.2.13 on 2022-07-21 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trackapi', '0005_auto_20220721_0018'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email address'),
        ),
    ]
