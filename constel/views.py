from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import FormCadastraUsuario, FormLogin, FormCadastraUsuarioPassivo, FormCadastrarVeiculo
from .models import UserType, Veiculo


@login_required()
def index(request):
    """
    View da página inicial do sistema
    :param request: None
    :return: Renderiza página inicial
    """

    context = {
        'admin': request.user.is_superuser,
    }

    return render(request, 'constel/index.html', context)


def view_cadastrar_usuario(request):
    """
    View de cadastro de novos usuários.
    :param request: POST form
    :return:
    """

    if request.method == 'POST':
        form = FormCadastraUsuario(request.POST)

        if form.is_valid():
            form.save()
            user = User.objects.get(username=form.cleaned_data['username'])
            modelo = form.cleaned_data['modelo']
            placa = form.cleaned_data['placa']
            cor = form.cleaned_data['cor']
            user_type = UserType(user=user)
            user_type.save()
            veiculo = Veiculo(user=user, modelo=modelo, placa=placa, cor=cor)
            veiculo.save()

            return HttpResponseRedirect('/login')
    else:
        form = FormCadastraUsuario()

    return render(request, 'constel/cadastra_usuario.html', {'form': form})


@login_required()
def view_cadastrar_usuario_passivo(request):
    """
    View de cadastro de novos usuários passivos.
    :param request: POST form
    :return:
    """

    if request.method == 'POST':
        form = FormCadastraUsuarioPassivo(request.POST)

        if form.is_valid():
            form.save()
            user = User.objects.get(username=form.cleaned_data['username'])
            modelo = form.cleaned_data['modelo']
            placa = form.cleaned_data['placa']
            cor = form.cleaned_data['cor']
            user_type = UserType(user=user)
            user_type.save()
            veiculo = Veiculo(user=user, modelo=modelo, placa=placa, cor=cor)
            veiculo.save()

            return HttpResponseRedirect('/gc/menu-cadastros/')
    else:
        form = FormCadastraUsuarioPassivo()

    return render(request, 'constel/cadastra_usuario_passivo.html', {'form': form})


@login_required()
def view_cadastrar_veiculo(request):
    """
    View de cadastro de veículos de funcionários existentes
    :param request:
    :return: formulário de cadastro
    """

    if request.method == 'POST':
        form = FormCadastrarVeiculo(request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/gc/menu-cadastros/')
    else:
        form = FormCadastrarVeiculo()

    return render(request, 'constel/cadastra_veiculo.html', {'form': form})


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

                    if user.user_type.is_passive:
                        messages.error(request, 'Usuário não autenticado, contate o administrador!')
                        return HttpResponseRedirect('/login')

                    else:
                        login(request, user)
                        return HttpResponseRedirect('/')

        else:
            form = FormLogin()

        return render(request, 'constel/login.html', {'form': form})


@login_required()
def view_consulta_funcionarios(request):

    users = User.objects.all().order_by('first_name')
    context = {
        'users': users,
    }

    return render(request, 'constel/consulta_funcionarios.html', context)


@login_required()
def view_consulta_veiculos(request):

    veiculos = Veiculo.objects.filter(user__is_active=True).order_by('user__first_name', 'user__last_name')
    context = {
        'veiculos': veiculos,
    }

    return render(request, 'constel/consulta_veiculos.html', context)


@login_required()
def view_logout(request):

    logout(request)
    return HttpResponseRedirect('/login/')
