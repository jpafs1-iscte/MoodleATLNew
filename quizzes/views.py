from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Quizz
from django.views.generic import ListView
from django.http import JsonResponse, HttpResponseRedirect
from questions.models import Question, Answer
from results.models import Result


# Create your views here.

class QuizListView(ListView):
    model = Quizz
    template_name = 'quizzes/main.html'


def quiz_view(request, pk):
    quizz = Quizz.objects.get(pk=pk)
    return render(request, 'quizzes/Quizzes.html', {'obj': quizz})


def quiz_data_view(request, pk):
    quiz = Quizz.objects.get(pk=pk)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): answers})
    return JsonResponse({
        'data': questions,
        'time': quiz.time,
    })


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def create_quiz(request):
    return render(request, 'quizzes/Create_Quiz.html')


def main_view(request):
    return render(request, 'quizzes/main.html')


def create_question(request):
    data = {'quizes': Quizz.objects.all()}
    return render(request, 'quizzes/Create_question.html', data)


def create_response(request):
    data = {'questions': Question.objects.all()}
    return render(request, 'quizzes/Create_response.html', data)


def QuizCreator(request):
    if request.method == 'POST':
        try:
            Quiz_name = request.POST.get("name")
            Quiz_topic = request.POST.get("topic")
            Quiz_number_of_questions = request.POST.get("number_of_questions")
            Quiz_time = request.POST.get("time")
            Quiz_score_to_pass = request.POST.get("score_to_pass")
            Quiz_diff = request.POST.get("diff")
        except KeyError:
            return render(request, 'atlmoodle:create_quiz')
        if Quiz_name and Quiz_topic and Quiz_number_of_questions and Quiz_time and Quiz_score_to_pass and Quiz_diff:
            Quiz = Quizz(name=Quiz_name, topic=Quiz_topic, number_of_questions=Quiz_number_of_questions, time=Quiz_time,
                         score_to_pass=Quiz_score_to_pass, diff=Quiz_diff)
            Quiz.save()
            return HttpResponseRedirect(reverse('atlmoodle:quizzes:main-view'))
        else:
            return HttpResponseRedirect(reverse('atlmoodle:quizzes:create_quiz'))
    else:
        return render(request, 'quizzes/main.html')


def QuestionCreator(request):
    if request.method == 'POST':
        try:
            Question_text = request.POST.get("question")
            Question_quiz = request.POST.get("quiz")

            quiz = get_object_or_404(Quizz, id=Question_quiz)
        except KeyError:
            return render(request, 'atlmoodle:create_question')

        if Question_text and quiz:
            question = Question(text=Question_text, quizz=quiz)
            question.save()
            return HttpResponseRedirect(reverse('atlmoodle:quizzes:main-view'))
        else:
            return HttpResponseRedirect(reverse('atlmoodle:quizzes:create_question'))
    else:
        return render(request, 'quizzes/main.html')


def ResponseCreator(request):
    if request.method == 'POST':
        try:
            Answer_text = request.POST.get("response")
            Answer_questions = request.POST.get("question")
            Answer_correct = request.POST.get("correct")
            if(Answer_correct == "on"):
                Answer_correct=True
            else:
                Answer_correct=False

            question = get_object_or_404(Question, id=Answer_questions)
        except KeyError:
            return render(request, 'atlmoodle:create_answer')

        if question and Answer_text:
            answer = Answer(text=Answer_text,question=question,correct=Answer_correct)
            answer.save()
            return HttpResponseRedirect(reverse('atlmoodle:quizzes:main-view'))
        else:
            return HttpResponseRedirect(reverse('atlmoodle:quizzes:create_response'))
    else:
        return render(request, 'quizzes/main.html')


def save_quiz_view(request, pk):
    if is_ajax(request):
        questions = []
        data = request.POST
        data_ = dict(data.lists())

        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            print('key: ', k)
            question = Question.objects.get(text=k)
            questions.append(question)
        print(questions)

        user = request.user
        quiz = Quizz.objects.get(pk=pk)

        score = 0
        multiplier = 100 / quiz.number_of_questions
        results = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.text)

            if a_selected != "":
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score += 1
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text

                results.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
            else:
                results.append({str(q): 'not answered'})

        score_ = score * multiplier
        Result.objects.create(quizz=quiz, user=user, score=score_)

        if score_ >= quiz.score_to_pass:
            return JsonResponse({'passed': True, 'score': score_, 'results': results})
        else:
            return JsonResponse({'passed': False, 'score': score_, 'results': results})
