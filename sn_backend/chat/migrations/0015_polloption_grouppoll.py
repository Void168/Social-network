# Generated by Django 4.2.6 on 2023-11-28 13:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0014_groupconversation_group_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PollOption',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('poll_option_name', models.TextField(default='', max_length=255)),
                ('users_vote', models.ManyToManyField(related_name='users_vote', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GroupPoll',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('poll_name', models.TextField(default='', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('time_end', models.DateTimeField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_create_poll', to=settings.AUTH_USER_MODEL)),
                ('poll_options', models.ManyToManyField(blank=True, to='chat.polloption')),
            ],
        ),
    ]
