from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import (
    FormCadastraUsuario,
    FormLogin
)
from .models import UserType, Veiculo
from .objects import Button
from .apps.controle_acessos.decorator import permission
from .menu import menu_principal


@login_required
@permission('admin', )
def view_menu_gerenciamento_sistema(request):
    button_1 = Button('constel_view_admin', 'Administração Django')
    button_2 = Button('constel_menu_controle_acessos', 'Controle de acessos')
    rollback = Button('index', 'Voltar')

    context = {
        'admin': request.user.is_superuser,
        'guia_titulo': 'Constel',
        'pagina_titulo': 'Constel',
        'buttons': [
            button_1,
            button_2,
        ],
        'rollback': rollback,
    }

    return render(request, 'constel/menu.html', context)


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

    context = {
        'form': form,
        'form_submit_text': 'Cadastrar-se',
    }

    return render(request, 'constel/v2/form_cadastro.html', context)


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

                        return HttpResponseRedirect(request.GET.get('next', '/'))
                
                else:
                    messages.error(request, 'Usuário e/ou senha incorretos!')

        else:
            form = FormLogin()

        return render(request, 'constel/v2/form_login.html', {'form': form})


@login_required
def view_consulta_funcionarios(request, rollback):

    users = User.objects.all().order_by('first_name', 'last_name')
    context = {
        'users': users,
        'pagina_titulo': 'Constel',
        'menu_titulo': 'Funcionários',
        'rollback': rollback,
    }

    return render(request, 'constel/consulta_funcionarios.html', context)


@login_required
def view_consulta_veiculos(request, rollback):

    veiculos = Veiculo.objects.filter(user__is_active=True).order_by('user__first_name', 'user__last_name')
    context = {
        'veiculos': veiculos,
        'pagina_titulo': 'Constel',
        'menu_titulo': 'Veículos',
        'rollback': rollback,
    }

    return render(request, 'constel/consulta_veiculos.html', context)


@login_required
def view_logout(request):

    logout(request)
    return HttpResponseRedirect('/login/')


@login_required
def indexv2(request):

    context = {
        'app': 'Constel',
    }

    return render(request, 'constel/v2/index.html', context)


@login_required
@permission('admin',)
def admin(request):
    context = menu_principal(request)

    return render(request, 'constel/v2/app.html', context)
