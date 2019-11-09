from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import FormCadastraUsuario, FormLogin
from .permissions import *


@login_required()
def index(request):
    """
    View da página inicial do sistema
    :param request: None
    :return: Renderiza página inicial
    """

    context = {
        'gerencia_gc': gerencia_gc(request.user),
        'gerencia_cont': gerencia_cont(request.user),
    }

    return render(request, 'constel/index.html', context)


def view_cadastrar_usuario(request):
    """
    View de cadastro de novos usuários.
    Cadastra usuários inativos, o adm deve validar os usuários!
    :param request: POST form
    :return:
    """

    if request.method == 'POST':
        form = FormCadastraUsuario(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            is_active = False

            user = User(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                is_active=is_active
            )
            user.save()

            return HttpResponseRedirect('/')

    else:
        form = FormCadastraUsuario()

    return render(request, 'constel/cadastra_usuario.html', {'form': form})


def view_login(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    else:

        if request.method == 'POST':
            form = FormLogin(request.POST)

            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)

                if user is not None:
                    login(request, user)

                    return HttpResponseRedirect('/')

        else:
            form = FormLogin()

        return render(request, 'constel/login.html', {'form': form})


@login_required()
def view_logout(request):

    logout(request)
    return HttpResponseRedirect('login')
