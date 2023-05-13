# Generated by Django 4.2.1 on 2023-05-09 21:50

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Questao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questao_texto', models.CharField(max_length=200)),
                ('pub_data', models.DateTimeField(verbose_name='data de publicacao')),
            ],
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anos_a_ensinar_min', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(9), django.core.validators.MinValueValidator(1)])),
                ('anos_a_ensinar_max', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(9), django.core.validators.MinValueValidator(1)])),
                ('contacto', models.IntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curso', models.CharField(max_length=100)),
                ('nr_votos', models.IntegerField(default=0)),
                ('image', models.TextField()),
                ('anoEscolar', models.IntegerField()),
                ('contacto', models.IntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]