# Generated by Django 4.2.6 on 2023-10-10 06:42

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.UUIDField(default=uuid.UUID('e03f1270-a956-4dd0-b0f6-0e64ce727054'), editable=False, primary_key=True, serialize=False),
        ),
    ]
