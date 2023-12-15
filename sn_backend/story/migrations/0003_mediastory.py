# Generated by Django 4.2.6 on 2023-12-12 10:25

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('story', '0002_storyattachment'),
    ]

    operations = [
        migrations.CreateModel(
            name='MediaStory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('caption', models.TextField(blank=True, null=True)),
                ('font', models.TextField(blank=True, default='Đơn giản', max_length=50)),
                ('theme', models.CharField(blank=True, max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('duaration', models.IntegerField(verbose_name=django.core.validators.MaxValueValidator(10))),
                ('is_private', models.BooleanField(default=False)),
                ('only_me', models.BooleanField(default=False)),
                ('seen_count', models.IntegerField(default=0)),
                ('attachments', models.ManyToManyField(blank=True, to='story.storyattachment')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='media_story', to=settings.AUTH_USER_MODEL)),
                ('seen_by', models.ManyToManyField(related_name='seen_media_story', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]