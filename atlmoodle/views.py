from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from .forms import CreateInForum, CreateInDiscussion
from .models import Aluno, Tutor, Event, forum, UploadedFile, TOPIC_CHOICES
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import *


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
        if 'useraluno' in request.POST:
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
                user = User.objects.create_user(username=nome, password=password, email=contacto, first_name=primeironome, last_name=ultimonome)
                user.save()
                aluno = Aluno.objects.create(user=user, first_name=primeironome, last_name=ultimonome, email=contacto, anoEscolar=ano)
                aluno.save()
                return HttpResponseRedirect(reverse('atlmoodle:loginpage'))
            else:

                return HttpResponseRedirect(reverse('atlmoodle:main_page'))
        elif 'usertutor' in request.POST:
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
                aluno = Tutor.objects.create(user=user, anos_a_ensinar_min=anomin, anos_a_ensinar_max=anomax)
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
    return HttpResponseRedirect(reverse('atlmoodle:loginpage'))


def detalhe(request):
    return render(request, 'atlmoodle/detalhe.html')


def eliminar(request):
    try:
        ficheiro_selecionado = UploadedFile.objects.get(pk=request.POST['ficheiro'])
    except (KeyError, UploadedFile.DoesNotExist):
        # Apresenta de novo o form para votar
        file = UploadedFile.objects.all()
        return render(request, 'atlmoodle/upload/eliminar_ficheiro.html',
                      {'ficheiros': file, 'error_message': "Não escolheu uma opção", })
    else:
        ficheiro_selecionado.delete()
    return HttpResponseRedirect(reverse('atlmoodle:main_page'))


def file(request):
    data = {
        "uploaded_files": UploadedFile.objects.all()
    }
    return render(request, "atlmoodle/upload/file.html", data)


def fazer_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        evento = request.POST.get('evento')
        titulo = request.POST.get('titulo')
        nome = request.user.first_name + request.user.last_name
        if request.user == Aluno:
            autor = "Aluno"
        else:
            autor = "Tutor"
        uploaded_file = UploadedFile(evento=evento, file=myfile, name=nome, autor=autor, titulo=titulo)
        uploaded_file.save()
        uploaded_files = UploadedFile.objects.all()
        return render(request, 'atlmoodle/upload/fazer_upload.html',
                      {'uploaded_file_url': uploaded_file_url,
                       'uploaded_files': uploaded_files})
    return render(request, 'atlmoodle/upload/fazer_upload.html')


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
        if request.user.is_authenticated:
            form = CreateInForum(request.POST)
            if form.is_valid():
                form.save(user=request.user)
                return redirect('/')
    context = {'form': form}
    return render(request, 'atlmoodle/forum/addForum.html', context)


def addInDiscussion(request):
    form = CreateInDiscussion()
    if request.method == 'POST':
        form = CreateInDiscussion(request.POST)
        if form.is_valid():
            form.save(user=request.user)
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
            event_category = request.POST.get("category")
        except KeyError:
            return render(request, 'atlmoodle/Calendar/CreateEvent.html', {'topic_choices': TOPIC_CHOICES})
        if event_name and event_description:
            evento = Event(name=event_name, description=event_description, created_at=timezone.now(), category=event_category)
            evento.save()
            return HttpResponseRedirect(reverse('atlmoodle:calendar_details', args=(evento.id,)))
        else:
            return HttpResponseRedirect(reverse('atlmoodle:eventCreator'))
    else:
        return render(request, 'atlmoodle/Calendar/CreateEvent.html', {'topic_choices': TOPIC_CHOICES})


@api_view(['GET', 'POST'])
def students_list(request):
    if request.method == 'GET':
        data = Aluno.objects.all()

        serializer = AlunoSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AlunoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
def students_detail(request, pk):
    try:
        student = Aluno.objects.get(pk=pk)
    except Aluno.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = AlunoSerializer(student, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)