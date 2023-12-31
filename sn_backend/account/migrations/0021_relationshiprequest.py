# Generated by Django 4.2.6 on 2023-11-09 14:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0020_alter_user_partner_alter_user_relationship_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelationshipRequest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('sent', 'Sent'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='sent', max_length=20)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_relationshiprequests', to=settings.AUTH_USER_MODEL)),
                ('created_for', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_relationshiprequests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
