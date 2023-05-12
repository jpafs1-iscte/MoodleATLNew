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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    anos_a_ensinar_min = models.IntegerField(default=1,validators=[MaxValueValidator(9), MinValueValidator(1)])
    anos_a_ensinar_max = models.IntegerField(default=1,validators=[MaxValueValidator(9), MinValueValidator(1)])

    def __str__(self):
        return self.user.username








