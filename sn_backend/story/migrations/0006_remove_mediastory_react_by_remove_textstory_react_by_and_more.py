# Generated by Django 4.2.6 on 2023-12-13 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0005_alter_reactstory_type_of_react'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mediastory',
            name='react_by',
        ),
        migrations.RemoveField(
            model_name='textstory',
            name='react_by',
        ),
        migrations.AddField(
            model_name='mediastory',
            name='reacted_by',
            field=models.ManyToManyField(null=True, related_name='react_media_story', to='story.reactstory'),
        ),
        migrations.AddField(
            model_name='textstory',
            name='reacted_by',
            field=models.ManyToManyField(related_name='react_text_story', to='story.reactstory'),
        ),
    ]
