# Generated by Django 4.2.6 on 2023-11-27 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0013_groupconversation_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupconversation',
            name='group_name',
            field=models.TextField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='groupconversation',
            name='name',
            field=models.TextField(default='', max_length=255),
        ),
    ]
