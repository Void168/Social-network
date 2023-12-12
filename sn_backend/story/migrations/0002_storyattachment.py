# Generated by Django 4.2.6 on 2023-12-12 10:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('story', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoryAttachment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(null=True, upload_to='story_attachments_image')),
                ('video', models.FileField(null=True, upload_to='story_attachments_video')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='story_attachments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
