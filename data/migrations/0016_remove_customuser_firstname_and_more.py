# Generated by Django 4.2.7 on 2025-04-07 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0015_alter_customuser_firstname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='firstname',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(max_length=20),
        ),
    ]
