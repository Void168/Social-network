# Generated by Django 4.2.6 on 2023-11-22 09:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0004_alter_conversationmessage_seen_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageAttachment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='message_attachments')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_attachments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='conversationmessage',
            name='attachments',
            field=models.ManyToManyField(blank=True, to='chat.messageattachment'),
        ),
    ]
