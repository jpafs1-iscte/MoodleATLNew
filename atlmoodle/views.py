from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .models import Aluno
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage


def index(request):
    return render(request, 'atlmoodle/index.html')


def detalhe(request, aluno_id):
    aluno = get_object_or_404(Aluno, pk=aluno_id)
    return render(request, 'atlmoodle/detalhe.html', {'aluno': aluno})


def main_page(request):
    return render(request, 'atlmoodle/index.html')


def go_quizzes(request):
    return render(request, 'quizzes/main.html')


# parte do login
def registo(request):
    if 'aluno-form' == 'POST':
        try:
            nome = request.POST.get('user')
            password = request.POST.get('pass')
            curso = request.POST.get('curso')
            ano = request.POST.get('anoEscolar')
            contacto = request.POST.get('contacto')

        except KeyError:
            return render(request, 'atlmoodle/registerpage.html')

        if nome and password and curso and ano and contacto:
            user = User.objects.create_user(nome, password)
            user.save()
            aluno = Aluno.objects.create(user=user, curso=curso, ano=ano, contacto=contacto)
            aluno.save()
            return HttpResponseRedirect(reverse('atlmoodle:loginpage'))
        else:
            return HttpResponseRedirect(reverse('atlmoodle:registerpage'))

    else:
        try:
            nome = request.POST.get('user')
            password = request.POST.get('pass')
            anomin = request.POST.get('anos_a_ensinar_min')
            anomax = request.POST.get('anos_a_ensinar_max')
            contacto = request.POST.get('contacto')

        except KeyError:
            return render(request, 'atlmoodle/registerpage.html')

        if nome and password and anomin and anomax and contacto:
            user = User.objects.create_user(nome, password)
            user.save()
            aluno = Aluno.objects.create(user=user, anomin=anomin, anomax=anomax, contacto=contacto)
            aluno.save()
            return HttpResponseRedirect(reverse('atlmoodle:loginpage'))
        else:
            return HttpResponseRedirect(reverse('atlmoodle:registerpage'))


def loginpage(request):
    if request.method == 'POST':
        try:
            nome = request.POST.get('nome')
            word = request.POST.get('word')
        except KeyError:
            return render(request, 'atlmoodle/loginpage.html')

        if nome and word:
            user = authenticate(username=nome, password=word)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('atlmoodle:index'))
            else:
                return HttpResponseRedirect(reverse('atlmoodle:registo'))
    else:
        return render(request, 'atlmoodle/loginpage.html')


def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('votacao:index'))


def personal(request):
    return render(request, 'votacao/personal.html')


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
        request.user.aluno.add_image("/atlmoodle/static/atlmoodle/images/" + filename)
        print(request.user.aluno.image)
        uploaded_file_url = fs.url(filename)
        return render(request, 'atlmoodle/fazer_upload.html',
                      {'uploaded_file_url': uploaded_file_url})
    return render(request, 'atlmoodle/fazer_upload.html')


def teste(request):
    return render(request, 'atlmoodle/teste.html')
