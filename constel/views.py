from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import FormCadastraUsuario, FormLogin, FormCadastraUsuarioPassivo, FormCadastrarVeiculo
from .models import UserType, Veiculo
from .objects import Button
from .apps.controle_acessos.decorator import permission

from .menu import menu_principal


@login_required
@permission('admin', )
def view_admin(request):

    return HttpResponseRedirect('/admin')


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


@login_required
def index(request):
    """
    View da página inicial do sistema
    :param request: None
    :return: Renderiza página inicial
    """

    button_1 = Button('almoxarifado_menu_principal', 'Almoxarifado')
    button_2 = Button('patrimonio_menu_principal', 'Patrimônio')
    button_3 = Button('constel_menu_admin', 'Administração do sistema')
    button_logout = Button('logout', 'Logout')

    context = {
        'admin': request.user.is_superuser,
        'guia_titulo': 'Constel',
        'pagina_titulo': 'Constel',
        'buttons': [
            button_1,
            button_2,
            button_3,
        ],
        'rollback': button_logout,
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
        'callback': 'login',
        'button_submit_text': 'Cadastrar-se',
        'callback_text': 'Cancelar',
        'pagina_titulo': 'Constel',
        'menu_titulo': 'Cadastro de funcionário',
    }

    return render(request, 'constel/cadastra_usuario.html', context)


@login_required
@permission('patrimonio - combustivel', )
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

            return HttpResponseRedirect('/patrimonio/combustivel/menu-cadastros/')
    else:
        form = FormCadastraUsuarioPassivo()

    context = {
        'form': form,
        'callback': 'gc_menu_cadastros',
        'button_submit_text': 'Cadastrar beneficiário',
        'callback_text': 'Cancelar',
        'pagina_titulo': 'Combustível',
        'menu_titulo': 'Cadastro de beneficiário',
    }

    return render(request, 'constel/cadastra_usuario_passivo.html', context)


@login_required
@permission('patrimonio - combustivel', )
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

            return HttpResponseRedirect('/patrimonio/combustivel/menu-cadastros/')
    else:
        form = FormCadastrarVeiculo()

    context = {
        'form': form,
        'callback': 'gc_menu_cadastros',
        'button_submit_text': 'Cadastrar veículo',
        'callback_text': 'Cancelar',
        'pagina_titulo': 'Combustível',
        'menu_titulo': 'Cadastro de veículo',
    }

    return render(request, 'constel/cadastra_veiculo.html', context)


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
                    messages.error(request, 'Usuário e/ou senha incorretos!')

        else:
            form = FormLogin()

        return render(request, 'constel/v2/login.html', {'form': form})


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
