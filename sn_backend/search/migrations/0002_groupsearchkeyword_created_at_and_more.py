# Generated by Django 4.2.6 on 2024-02-19 08:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupsearchkeyword',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='searchkeyword',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
