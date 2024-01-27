# Generated by Django 4.2.6 on 2024-01-27 10:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0025_alter_pageconversationmessage_created_by_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pageconversationmessage',
            name='seen_by',
        ),
        migrations.RemoveField(
            model_name='pageconversationmessage',
            name='seen_by_page',
        ),
        migrations.AddField(
            model_name='pageconversationmessage',
            name='seen_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_seen_message', to='chat.seenuser'),
        ),
        migrations.AddField(
            model_name='pageconversationmessage',
            name='seen_by_page',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='page_seen_message', to='chat.seenpage'),
        ),
    ]
