# Generated by Django 4.2.6 on 2023-11-18 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0014_tag_comment_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='tags',
        ),
    ]
