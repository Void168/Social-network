# Generated by Django 4.2.6 on 2024-01-05 09:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0019_alter_storyattachment_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediastory',
            name='duaration',
            field=models.FloatField(default=10, verbose_name=django.core.validators.MaxValueValidator(20)),
        ),
        migrations.AlterField(
            model_name='storyattachment',
            name='image',
            field=models.ImageField(blank=True, default='', null=True, upload_to='story_attachments_image'),
        ),
        migrations.AlterField(
            model_name='storyattachment',
            name='video',
            field=models.FileField(blank=True, default='', null=True, upload_to='story_attachments_video'),
        ),
    ]