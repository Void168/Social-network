# Generated by Django 4.2.6 on 2023-10-25 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_alter_conversationmessage_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversationmessage',
            name='is_last_message',
            field=models.BooleanField(default=False),
        ),
    ]
