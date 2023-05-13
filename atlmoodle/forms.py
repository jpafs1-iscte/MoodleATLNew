from django.forms import ModelForm
from .models import *


class CreateInForum(ModelForm):
    class Meta:
        model = forum
        fields = ('topic', 'description')

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        if user:
            instance.user = user.username
        if commit:
            instance.save()
        return instance


class CreateInDiscussion(ModelForm):
    class Meta:
        model = Discussion
        fields = "__all__"