# Generated by Django 4.2.6 on 2023-10-24 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0007_trend'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
    ]
