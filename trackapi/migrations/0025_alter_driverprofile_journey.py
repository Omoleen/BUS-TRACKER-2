# Generated by Django 4.0.6 on 2022-07-25 10:59

from django.db import migrations
import sortedm2m.fields
from sortedm2m.operations import AlterSortedManyToManyField


class Migration(migrations.Migration):

    dependencies = [
        ('trackapi', '0024_alter_driverprofile_journey'),
    ]

    operations = [
        AlterSortedManyToManyField(
            model_name='driverprofile',
            name='journey',
            field=sortedm2m.fields.SortedManyToManyField(help_text=None, to='trackapi.route'),
        ),
    ]
