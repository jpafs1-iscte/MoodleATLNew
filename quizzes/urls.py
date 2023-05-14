from django.urls import path
from .views import (
    QuizListView,
    quiz_view,
    quiz_data_view,
    save_quiz_view, create_quiz, QuizCreator,
)

app_name = 'quizzes'

urlpatterns = [
    path('', QuizListView.as_view(), name='main-view'),
    path('create_quiz', create_quiz, name='create_quiz'),
    path('QuizCreator', QuizCreator, name='QuizCreator'),
    path('<pk>/', quiz_view, name='quiz-view'),
    path('<pk>/save/', save_quiz_view, name='save-view'),
    path('<pk>/data/', quiz_data_view, name='quiz-data-view'),
]
