# Generated by Django 4.2.6 on 2024-02-03 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0007_group_anonymous_post_group_anyone_can_join_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='moderators',
            field=models.ManyToManyField(related_name='group_moderators', to='group.member'),
        ),
    ]
