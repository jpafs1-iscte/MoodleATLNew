# Generated by Django 4.1.7 on 2023-05-12 18:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('atlmoodle', '0002_delete_questao'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aluno',
            name='contacto',
        ),
        migrations.RemoveField(
            model_name='aluno',
            name='curso',
        ),
        migrations.RemoveField(
            model_name='aluno',
            name='image',
        ),
        migrations.RemoveField(
            model_name='aluno',
            name='nr_votos',
        ),
        migrations.RemoveField(
            model_name='tutor',
            name='contacto',
        ),
    ]