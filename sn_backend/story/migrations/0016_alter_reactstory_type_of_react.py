# Generated by Django 4.2.6 on 2024-01-03 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0015_alter_reactstory_type_of_react'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reactstory',
            name='type_of_react',
            field=models.CharField(choices=[('👍', '👍'), ('❤️', '❤️'), ('😍', '😍'), ('😆', '😆'), ('😲', '😲'), ('😥', '😥'), ('😡', '😡')], max_length=50),
        ),
    ]
