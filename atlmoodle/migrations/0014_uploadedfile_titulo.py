# Generated by Django 4.1.7 on 2023-05-14 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atlmoodle', '0013_tutor_user_uploadedfile_autor_uploadedfile_evento_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedfile',
            name='titulo',
            field=models.CharField(default='', max_length=255),
        ),
    ]
