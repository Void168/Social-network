# Generated by Django 4.2.6 on 2023-11-14 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('information', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='phonenumber',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='phonenumber',
            name='only_me',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='website',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='website',
            name='only_me',
            field=models.BooleanField(default=False),
        ),
    ]
