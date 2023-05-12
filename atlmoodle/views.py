from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from .forms import CreateInForum, CreateInDiscussion
from .models import Aluno, Event, forum
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage


def index(request):
    return render(request, 'atlmoodle/index.html')


# def detalhe(request, aluno_id):
#     aluno = get_object_or_404(Aluno, pk=aluno_id)
#     return render(request, 'atlmoodle/detalhe.html', {'aluno': aluno})


def main_page(request):
    return render(request, 'atlmoodle/index.html')


def go_quizzes(request):
    return render(request, 'quizzes/main.html')


# parte do login
def registo(request):
    if request.method == 'POST':
        print(request.POST['useraluno'])
        if request.POST['useraluno'] != "":
            try:
                nome = request.POST.get('useraluno')
                primeironome = request.POST.get('primeironome')
                ultimonome = request.POST.get('ultimonome')
                password = request.POST.get('pass')
                ano = request.POST.get('anoEscolar')
                contacto = request.POST.get('contacto')

            except KeyError:
                return render(request, 'atlmoodle/registerpage.html')

            if nome and primeironome and ultimonome and password and ano and contacto:
                user = User.objects.create_user(username=nome, email=contacto, password=password, first_name=primeironome, last_name=ultimonome)
                user.save()
                aluno = Aluno.objects.create(user=user, anoEscolar=ano)
                aluno.save()
                return HttpResponseRedirect(reverse('atlmoodle:loginpage'))
            else:

                return HttpResponseRedirect(reverse('atlmoodle:main_page'))

        else:
            try:
                nome = request.POST.get('usertutor')
                primeironome = request.POST.get('primeironome')
                ultimonome = request.POST.get('ultimonome')
                password = request.POST.get('pass')
                anomin = request.POST.get('anos_a_ensinar_min')
                anomax = request.POST.get('anos_a_ensinar_max')
                contacto = request.POST.get('contacto')

            except KeyError:
                return render(request, 'atlmoodle/registerpage.html')

            if nome and primeironome and ultimonome and password and anomin and anomax and contacto:
                user = User.objects.create_user(username=nome, email=contacto, password=password, first_name=primeironome, last_name=ultimonome)
                user.save()
                aluno = Aluno.objects.create(user=user, anomin=anomin, anomax=anomax)
                aluno.save()
                return HttpResponseRedirect(reverse('atlmoodle:loginpage'))
            else:
                return HttpResponseRedirect(reverse('atlmoodle:main_page'))

    return render(request, 'atlmoodle/registerpage.html')


def loginpage(request):
    if request.method == 'POST':
        try:
            nome = request.POST.get('user')
            password = request.POST.get('pass')
        except KeyError:
            return render(request, 'atlmoodle/loginpage.html')

        if nome and password:
            user = authenticate(username=nome, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('atlmoodle:main_page'))
            else:
                return HttpResponseRedirect(reverse('atlmoodle:registo'))
    else:
        return render(request, 'atlmoodle/loginpage.html')


def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('atlmoodle:main_page'))


def detalhe(request):
    return render(request, 'atlmoodle/detalhe.html')


def eliminar(request):
    try:
        questao_seleccionada = Questao.objects.get(pk=request.POST['questao'])
    except (KeyError, Questao.DoesNotExist):
        # Apresenta de novo o form para votar
        questoes = Questao.objects.all()
        return render(request, 'votacao/eliminarQuestao.html',
                      {'questoes': questoes, 'error_message': "Não escolheu uma opção", })
    else:
        questao_seleccionada.delete()
        # Retorne sempre HttpResponseRedirect depois de
        # tratar os dados POST de um form
        # pois isso impede os dados de serem tratados
        # repetidamente se o utilizador
        # voltar para a página web anterior.
    return HttpResponseRedirect(reverse('votacao:index'))


def fazer_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'atlmoodle/fazer_upload.html',
                      {'uploaded_file_url': uploaded_file_url})
    return render(request, 'atlmoodle/fazer_upload.html')


def teste(request):
    return render(request, 'atlmoodle/teste.html')

def home(request):
    forums = forum.objects.all()
    count = forums.count()
    discussions = []
    for i in forums:
        discussions.append(i.discussion_set.all())

    context = {'forums': forums,
               'count': count,
               'discussions': discussions}
    return render(request, 'atlmoodle/forum/Forum.html', context)


def addInForum(request):
    form = CreateInForum()
    if request.method == 'POST':
        form = CreateInForum(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'atlmoodle/forum/addForum.html', context)


def addInDiscussion(request):
    form = CreateInDiscussion()
    if request.method == 'POST':
        form = CreateInDiscussion(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'atlmoodle/forum/discussion.html', context)

def calendar(request):
    data = {
        "events": Event.objects.all,
    }
    return render(request, "atlmoodle/Calendar/Calendar.html", data)

def calendar_details(request, event_id):
    evento = get_object_or_404(Event, pk=event_id)
    return render(request, 'atlmoodle/Calendar/CalendarDetails.html', {'evento': evento})

def eventCreator(request):
    if request.method == 'POST':
        try:
            event_name = request.POST.get("name")
            event_description = request.POST.get("description")
        except KeyError:
            return render(request, 'atlmoodle/Calendar/CreateEvent.html')
        if event_name and event_description:
            evento = Event(name=event_name, description=event_description, created_at=timezone.now())
            evento.save()
            return HttpResponseRedirect(reverse('atlmoodle:calender_details', args=(evento.id,)))
        else:
            return HttpResponseRedirect(reverse('atlmoodle:eventCreator'))
    else:
        return render(request, 'atlmoodle/Calendar/CreateEvent.html')
