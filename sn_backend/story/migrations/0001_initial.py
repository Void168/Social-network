# Generated by Django 4.2.6 on 2023-12-12 10:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TextStory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('body', models.TextField(blank=True)),
                ('font', models.TextField(blank=True, default='Đơn giản', max_length=50)),
                ('theme', models.CharField(blank=True, default='Cổ điển', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('duaration', models.IntegerField(default=10)),
                ('is_private', models.BooleanField(default=False)),
                ('only_me', models.BooleanField(default=False)),
                ('seen_count', models.IntegerField(default=0)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='text_story', to=settings.AUTH_USER_MODEL)),
                ('seen_by', models.ManyToManyField(related_name='seen_text_story', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
