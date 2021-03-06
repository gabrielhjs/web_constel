from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Count, Sum
from django.core.paginator import Paginator

from .forms import (
    FormCadastraUsuario,
    FormLogin,
    FormFiltraQ,
    FormUsuarioEdita,
    FormUsuarioSenha,
    FormCadastraUsuarioPassivo
)
from .models import UserType, Veiculo
from .apps.controle_acessos.decorator import permission
from .menu import menu_principal, menu_cadastros


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


@login_required
@permission('admin',)
def cadastros(request):
    context = menu_cadastros(request)

    return render(request, 'constel/v2/app.html', context)


@login_required
@permission('admin',)
def usuarios(request):
    menu = menu_principal(request)

    q = request.GET.get('q', '')

    initial = {
        'q': q
    }

    form = FormFiltraQ(
        initial=initial,
        descricao='Nome ou matrícula'
    )

    query = Q()

    if q != '':
        query = query & Q(
            Q(username__icontains=q) |
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q))

    itens = User.objects.filter(
        query
    ).values(
        'username',
        'first_name',
        'last_name',
        'last_login',
        'user_type__is_passive',
    ).order_by(
        'first_name',
        'last_name',
    )

    paginator = Paginator(itens, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form': form,
        'form_submit_text': 'Filtrar',
    }
    context.update(menu)

    return render(request, 'constel/v2/usuarios.html', context)


@login_required
@permission('admin',)
def usuarios_edita(request, matricula):
    menu = menu_principal(request)

    user = get_object_or_404(User, username=matricula)
    form = FormUsuarioEdita(request.POST or None, request.FILES or None, instance=user)

    if request.method == 'POST':

        if matricula == 'admin':
            messages.error(request, 'Negado')

            return HttpResponseRedirect(
                f'/administracao/usuarios/{matricula}?{request.GET.urlencode()}'
            )

        if form.is_valid():
            form.save()



            return HttpResponseRedirect(
                f'/administracao/usuarios/{form.cleaned_data["username"]}?{request.GET.urlencode()}'
            )

    context = {
        'form': form,
        'form_submit_text': 'Salvar edição',
        'user_id': user.id,
    }
    context.update(menu)

    return render(request, 'constel/v2/usuarios_edita.html', context)


@login_required
@permission('admin',)
def usuarios_info(request, matricula):
    menu = menu_principal(request)

    get_object_or_404(User, username=matricula)

    taloes = User.objects.filter(username=matricula).values(
        'talao_user_to__talao__talao',
        'talao_user_to__user__first_name',
        'talao_user_to__user__last_name',
        'talao_user_to__data',
    ).annotate(
        n_vales=Count('talao_user_to__talao__talao_vales', filter=Q(talao_user_to__talao__talao_vales__status=2)),
        valor_agregado=Sum('talao_user_to__talao__talao_vales__vale_entrega__valor'),
    ).exclude(
        talao_user_to__talao__talao=None
    ).order_by(
        '-talao_user_to__data'
    )

    vales = User.objects.filter(username=matricula).values(
        'vale_user_to__vale__vale',
        'vale_user_to__user__first_name',
        'vale_user_to__user__last_name',
        'vale_user_to__data',
        'vale_user_to__valor',
    ).exclude(
        vale_user_to__vale__vale=None
    ).order_by(
        '-vale_user_to__data'
    )

    vales_total = vales.aggregate(
        quantidade=Count('vale_user_to__vale__vale'),
        total=Sum('vale_user_to__valor'),
    )

    materiais = User.objects.filter(username=matricula).values(
        'almoxarifado_retiradas__material__codigo',
        'almoxarifado_retiradas__material__material',
    ).annotate(
        quantidade=Sum('almoxarifado_retiradas__quantidade')
    ).exclude(
        almoxarifado_retiradas__material__codigo=None
    ).order_by(
        'almoxarifado_retiradas__material__material'
    )

    context = {
        'taloes': taloes,
        'vales': vales,
        'vales_total': vales_total,
        'materiais': materiais,
    }
    context.update(menu)

    return render(request, 'constel/v2/usuarios_info.html', context)


@login_required
@permission('admin',)
def usuarios_senha(request, user):
    menu = menu_principal(request)

    user = get_object_or_404(User, id=user)
    form = FormUsuarioSenha(user=user, data=request.POST or None)

    if request.method == 'POST':

        if user.username == 'admin':
            messages.error(request, 'Negado')

            return HttpResponseRedirect(
                f'/administracao/usuarios/senha/{str(user.id)}/?{request.GET.urlencode()}'
            )

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Senha alterada com sucesso')

            return HttpResponseRedirect(
                f'/administracao/usuarios/{str(user.username)}?{request.GET.urlencode()}'
            )

    context = {
        'form': form,
        'form_submit_text': 'Alterar senha',
        'user_username': user.username,
    }
    context.update(menu)

    return render(request, 'constel/v2/usuarios_senha.html', context)


@login_required()
@permission('admin',)
def cadastrar_usuario_passivo(request):
    """
    View de carregamento e gestão do cadastro de usuários passivos que não acessam o sistema,
    Deve ser acessada somente pelo adm e funcionários autorizados
    :param request: informações do formulário
    :return: carregamento do formulário
    """
    menu = menu_cadastros(request)

    if request.method == 'POST':
        form = FormCadastraUsuarioPassivo(request.POST)

        if form.is_valid():
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

                messages.success(request, 'Funcionário cadastrado com sucesso')

                return HttpResponseRedirect('/administracao/usuarios/cadastro/sem_acesso')
    else:
        form = FormCadastraUsuarioPassivo()

    context = {
        'form': form,
        'form_submit_text': 'Cadastrar usuário sem acesso',
    }
    context.update(menu)

    return render(request, 'talao/v2/cadastrar_talao.html', context)
