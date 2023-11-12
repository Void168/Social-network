# Generated by Django 4.2.6 on 2023-11-12 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0025_phonenumber'),
    ]

    operations = [
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('is_private', models.BooleanField(default=True)),
                ('only_me', models.BooleanField(default=False)),
            ],
        ),
    ]
