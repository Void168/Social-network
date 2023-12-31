# Generated by Django 4.2.6 on 2024-01-06 10:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0033_user_is_online'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='followers_count',
            field=models.IntegerField(default=0),
        ),
    ]
