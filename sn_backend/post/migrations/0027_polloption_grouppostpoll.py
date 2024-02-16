# Generated by Django 4.2.6 on 2024-02-12 14:52

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0010_remove_group_questions_remove_group_rules_and_more'),
        ('post', '0026_grouppost_is_anonymous'),
    ]

    operations = [
        migrations.CreateModel(
            name='PollOption',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('body', models.TextField(blank=True, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='create_poll', to='group.member')),
            ],
        ),
        migrations.CreateModel(
            name='GroupPostPoll',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('body', models.TextField(blank=True, null=True)),
                ('is_anonymous', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('pending', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_post_polls', to='group.member')),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='group_own_poll', to='group.group')),
                ('options', models.ManyToManyField(blank=True, to='post.polloption')),
                ('reported_by_members', models.ManyToManyField(blank=True, to='group.member')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]