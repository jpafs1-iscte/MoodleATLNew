import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime

class Aluno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    curso = models.CharField(max_length=100)
    nr_votos = models.IntegerField(default=0)
    image = models.TextField()
    anoEscolar = models.IntegerField()
    contacto = models.IntegerField()

    def __str__(self):
        return self.user.username

    def getContacto(self):
        return self.contacto

    def add_voto(self):
        self.nr_votos += 1
        self.save()

    def add_image(self, image):
        self.image = image
        self.save()

    def remove_image(self):
        self.delete()

class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    anos_a_ensinar_min = models.IntegerField(default=1,validators=[MaxValueValidator(9), MinValueValidator(1)])
    anos_a_ensinar_max = models.IntegerField(default=1,validators=[MaxValueValidator(9), MinValueValidator(1)])
    contacto = models.IntegerField()

    def __str__(self):
        return self.user.username








