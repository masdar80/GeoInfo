# Generated by Django 3.1 on 2021-12-19 15:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('observe', '0003_auto_20211219_1510'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fieldparameter',
            old_name='sample_id',
            new_name='watersampling',
        ),
    ]
