# Generated by Django 4.2.6 on 2024-01-03 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0011_alter_mediastory_duaration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reactstory',
            name='type_of_react',
            field=models.CharField(choices=[('👍', 'Like react'), ('❤️', 'Heart react'), ('😍', 'Love react'), ('😆', 'Laugh react'), ('😲', 'Suprise react'), ('😥', 'Sad react'), ('😡', 'Angry react')], max_length=50),
        ),
    ]
