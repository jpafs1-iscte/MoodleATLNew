from django.db import models
from django.utils import timezone
from django.utils.datetime_safe import datetime
from quizzes.models import Quizz


# Create your models here.
class Question(models.Model):
    text = models.CharField(max_length=200)
    quizz = models.ForeignKey(Quizz, on_delete=models.CASCADE)
    pub_data = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    def foi_publicada_recentemente(self):
        return self.pub_data >= timezone.now() - datetime.timedelta(days=1)

    def get_answers(self):
        return self.answer_set.all()


class Answer(models.Model):
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    pub_data = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"question: {self.question.text}, answer: {self.text}, correct:{self.correct}"
