# Generated by Django 5.1.7 on 2025-03-27 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='dni',
            field=models.CharField(max_length=8, unique=True),
        ),
    ]
