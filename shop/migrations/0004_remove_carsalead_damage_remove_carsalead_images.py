# Generated by Django 5.0.6 on 2025-06-06 11:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_carbrand_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carsalead',
            name='damage',
        ),
        migrations.RemoveField(
            model_name='carsalead',
            name='images',
        ),
    ]
