# Generated by Django 2.1.4 on 2018-12-23 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0009_auto_20181223_1730'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='position',
            new_name='job',
        ),
    ]
