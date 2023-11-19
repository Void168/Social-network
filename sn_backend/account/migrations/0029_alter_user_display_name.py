# Generated by Django 4.2.6 on 2023-11-19 11:26

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0028_alter_user_display_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='display_name',
            field=models.CharField(blank=True, default=uuid.uuid4, max_length=255),
        ),
    ]
