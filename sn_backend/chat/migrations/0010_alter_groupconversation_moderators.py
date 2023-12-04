# Generated by Django 4.2.6 on 2023-11-25 20:00

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0009_alter_groupconversation_moderators'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupconversation',
            name='moderators',
            field=models.ManyToManyField(related_name='moderators_groupchat', to=settings.AUTH_USER_MODEL),
        ),
    ]