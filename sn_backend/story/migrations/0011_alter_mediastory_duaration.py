# Generated by Django 4.2.6 on 2023-12-18 10:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0010_alter_storyattachment_rotate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediastory',
            name='duaration',
            field=models.IntegerField(default=10, verbose_name=django.core.validators.MaxValueValidator(20)),
        ),
    ]