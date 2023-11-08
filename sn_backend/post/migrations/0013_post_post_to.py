# Generated by Django 4.2.6 on 2023-11-06 10:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0012_alter_comment_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post_to', to=settings.AUTH_USER_MODEL),
        ),
    ]