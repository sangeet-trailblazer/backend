# Generated by Django 4.2.7 on 2025-07-11 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0019_otpstore'),
    ]

    operations = [
        migrations.AddField(
            model_name='otpstore',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default='2024-01-01 00:00:00'),
            preserve_default=False,
        ),
    ]
