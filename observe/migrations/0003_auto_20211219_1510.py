# Generated by Django 3.1 on 2021-12-19 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('observe', '0002_waterchemistrysurvey_station_created_by'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fieldparameter',
            old_name='watersampling',
            new_name='sample_id',
        ),
    ]
