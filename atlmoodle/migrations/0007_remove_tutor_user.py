# Generated by Django 4.1.7 on 2023-05-13 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('atlmoodle', '0006_remove_forum_name_forum_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tutor',
            name='user',
        ),
    ]
