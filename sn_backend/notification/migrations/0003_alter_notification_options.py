# Generated by Django 4.2.6 on 2023-10-31 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_alter_notification_type_of_notification'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ('-created_at',)},
        ),
    ]
