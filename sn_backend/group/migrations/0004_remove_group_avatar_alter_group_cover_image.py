# Generated by Django 4.2.6 on 2024-01-28 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0003_member_last_access_pagemember_last_access'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='avatar',
        ),
        migrations.AlterField(
            model_name='group',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='group_cover_images'),
        ),
    ]
