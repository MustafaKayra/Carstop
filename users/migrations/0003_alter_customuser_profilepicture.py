# Generated by Django 5.0.6 on 2025-06-18 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_biography_customuser_gsmnumber_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profilepicture',
            field=models.ImageField(blank=True, null=True, upload_to='profilepicture/', verbose_name='Profil Fotoğrafı'),
        ),
    ]
