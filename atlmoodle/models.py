import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime

class Aluno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    anoEscolar = models.IntegerField()

    def __str__(self):
        return self.user.username


class Tutor(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    anos_a_ensinar_min = models.IntegerField(default=1,validators=[MaxValueValidator(9), MinValueValidator(1)])
    anos_a_ensinar_max = models.IntegerField(default=1,validators=[MaxValueValidator(9), MinValueValidator(1)])

    def __str__(self):
        return self.user.username


class forum(models.Model):
    user = models.CharField(max_length=300, default="")
    topic = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.topic)


# child model
class Discussion(models.Model):
    user = models.CharField(max_length=300, default="")
    forum = models.ForeignKey(forum, blank=True, on_delete=models.CASCADE)
    discuss = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.forum)


TOPIC_CHOICES = (
    ('testes', 'Testes'),
    ('visitas', 'Visitas de Estudo'),
    ('feriados', 'Feriados'),
    ('greves', 'Greves'),
    ('ferias', 'Férias'),
)

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField('data de publicação')
    category = models.CharField(max_length=20, choices=TOPIC_CHOICES, default='testes')

    def __str__(self):
        return self.name


class UploadedFile(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')

    def __str__(self):
        return self.name




