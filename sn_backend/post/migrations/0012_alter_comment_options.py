# Generated by Django 4.2.6 on 2023-11-02 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0011_post_only_me'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('-created_at',)},
        ),
    ]
