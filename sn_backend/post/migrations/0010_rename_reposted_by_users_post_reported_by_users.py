# Generated by Django 4.2.6 on 2023-10-24 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0009_post_reposted_by_users'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='reposted_by_users',
            new_name='reported_by_users',
        ),
    ]
