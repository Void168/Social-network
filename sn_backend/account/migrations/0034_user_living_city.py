# Generated by Django 4.2.6 on 2023-11-14 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0033_delete_livedcity'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='living_city',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
