# Generated by Django 4.2.6 on 2023-11-19 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0027_user_display_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='display_name',
            field=models.CharField(blank=True, default='user<function uuid4 at 0x000002CD6DAA7740>', max_length=255),
        ),
    ]
