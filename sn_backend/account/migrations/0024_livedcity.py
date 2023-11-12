# Generated by Django 4.2.6 on 2023-11-12 14:48

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0023_alter_relationshiprequest_relationship_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='LivedCity',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, default='', max_length=255)),
                ('year_start', models.CharField(blank=True, default='', max_length=255)),
                ('year_end', models.CharField(blank=True, default='', max_length=255)),
            ],
        ),
    ]
