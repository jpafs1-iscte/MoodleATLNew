from rest_framework import serializers
from .models import Aluno

class AlunoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Aluno
        fields = ('pk', 'user', 'first_name', 'last_name', 'email', 'anoEscolar')