# Generated by Django 4.2.6 on 2023-11-30 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0021_groupnotification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupnotification',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
