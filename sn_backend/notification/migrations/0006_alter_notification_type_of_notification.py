# Generated by Django 4.2.6 on 2023-11-18 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0005_alter_notification_type_of_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='type_of_notification',
            field=models.CharField(choices=[('new_friend_request', 'New friendrequest'), ('accepted_relationship_request', 'Accepted friendrequest'), ('rejected_relationship_request', 'Rejected friendrequest'), ('post_like', 'Post like'), ('post_comment', 'Post comment'), ('tag_comment', 'Tag comment'), ('new_relationship_request', 'Relationship request')], max_length=50),
        ),
    ]
