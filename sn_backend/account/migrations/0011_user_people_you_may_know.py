# Generated by Django 4.2.6 on 2023-10-21 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_user_posts_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='people_you_may_know',
            field=models.IntegerField(default=0),
        ),
    ]
