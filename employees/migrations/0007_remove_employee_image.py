# Generated by Django 2.1.4 on 2018-12-20 18:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0006_auto_20181220_1758'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='image',
        ),
    ]