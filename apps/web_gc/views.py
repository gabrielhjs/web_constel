from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Sum
from django.shortcuts import get_object_or_404

from .forms import FormTalao, FormEntregaTalao, FormEntregaVale, FormCadastraCombustivel, FormTest
from .models import Talao, Vale, CadastroTalao, EntregaTalao, EntregaVale, Combustivel
from .permissions import *


@login_required()
@permission_required(
    (
        'web_gc.add_talao',
        'web_gc.add_vale',
        'web_gc.add_entregatalao',
    ),
    raise_exception=True)
def view_cadastrar_talao(request):
    """
    View de carregamento e gestão do cadastro de novos talões,
    Deve ser acessada somente pelo adm e funcionários autorizados
    :param request: informações do formulário
    :return: carregamento do formulário
    """

    if request.method == 'POST':
        form = FormTalao(request.POST)

        if form.is_valid():
            # Registro do cadastro do novo talão
            form.save()
            talao = Talao.objects.get(talao=form.cleaned_data['talao'])
            cadastro_talao = CadastroTalao(talao=talao, user=request.user)

            try:
                for i in range(form.cleaned_data['vale_inicial'], form.cleaned_data['vale_final'] + 1):
                    vale = Vale(vale=i, status=0, talao=talao)
                    vale.save()

            except IntegrityError:
                talao.delete()
                cadastro_talao.delete()
                return HttpResponseRedirect('/gc/menu-cadastros/cadastro-talao')

            cadastro_talao.save()
            return HttpResponseRedirect('/gc/menu-cadastros')

    else:
        form = FormTalao()

    return render(request, 'web_gc/cadastro_talao.html', {'form': form})


@login_required()
@permission_required(
    (
        'web_gc.add_combustivel',
    ),
    raise_exception=True)
def view_cadastrar_combustivel(request):
    """
    View de carregamento e gestão de combustível novos cadastrados no sistema,
    deve ser acessado apenas pelo adm e funcionãrios autorizados
    :param request: informações do formulário
    :return: carregamento do formulário
    """

    if request.method == 'POST':
        # Registro do cadastro do combustível
        form = FormCadastraCombustivel(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/gc/menu-cadastros')
    else:
        form = FormCadastraCombustivel()

    context = {
        'combustiveis': Combustivel.objects.all(),
        'form': form,
    }

    return render(request, 'web_gc/cadastro_combustivel.html', context)


@login_required()
@permission_required(
    (
        'web_gc.change_talao',
        'web_gc.add_entregatalao',
    ),
    raise_exception=True)
def view_entrega_talao(request):
    """
    View de carregamento e gestão de entrega de talões cadastrados no sistema,
    deve ser acessado apenas pelo adm e funcionãrios autorizados
    :param request: informações do formulário
    :return: carregamento do formulário
    """

    if request.method == 'POST':
        # Registro da entrega do talão
        form = FormEntregaTalao(request.POST)

        if form.is_valid():
            talao = form.cleaned_data['talao']
            talao.status = 1
            Vale.objects.filter(talao=talao).update(status=1)
            entrega_talao = EntregaTalao(
                talao=talao,
                user=request.user,
                user_to=form.cleaned_data['user_to'],
            )
            entrega_talao.save()
            talao.save()
            return HttpResponseRedirect('/gc/menu-taloes')
    else:
        form = FormEntregaTalao()

    return render(request, 'web_gc/entrega_talao.html', {'form': form})


@login_required()
@permission_required(
    (
        'web_gc.change_vale',
        'web_gc.add_entregavale',
    ),
    raise_exception=True)
def view_entrega_vale(request):
    """
    View de carregamento e gestão de entrega de vales cadastrados no sistema,
    deve ser acessado apenas pelo adm e funcionãrios autorizados
    :param request: informações do formulário
    :return: carregamento do formulário
    """

    if request.method == 'POST':
        form = FormEntregaVale(request.user, request.POST)

        if form.is_valid():
            # Registro da entrega do vale

            vale = form.cleaned_data['vale']
            vale.status = 2
            entrega_vale = EntregaVale(
                vale=vale,
                user=request.user,
                user_to=form.cleaned_data['user_to'],
                combustivel=form.cleaned_data['combustivel'],
                valor=form.cleaned_data['valor'],
                observacao=form.cleaned_data['observacao'],
            )
            entrega_vale.save()
            vale.save()
            return HttpResponseRedirect('/gc/menu-vales')

    else:
        form = FormEntregaVale(request.user)

    return render(request, 'web_gc/entrega_vale.html', {'form': form})


@login_required()
def view_menu_principal(request):
    """
    View de carregamento da página inicial do GC
    :param request: informações gerais
    :return: carregamento da página inicial
    """

    context = {
        'gerencia_talao': combustivel_gerencia_talao(request.user),
        'gerencia_vale': combustivel_gerencia_vale(request.user),
        'beneficiario': combustivel_beneficiario(request.user),
    }

    return render(request, 'web_gc/menu_principal.html', context)


@login_required()
def view_menu_cadastros(request):
    """
    View de carregamento da página de cadastros do GC
    :param request: informações gerais
    :return: carregamento da página de cadastro
    """

    context = {
        'gerencia_talao': combustivel_gerencia_talao(request.user),
        'gerencia_vale': combustivel_gerencia_vale(request.user),
        'beneficiario': combustivel_beneficiario(request.user),
    }

    return render(request, 'web_gc/menu_cadastros.html', context)


@login_required()
def view_menu_consultas(request):
    """
    View de carregamento da página de consultas do GC
    :param request: informações gerais
    :return: carregamento da página de consultas
    """

    context = {
        'gerencia_talao': combustivel_gerencia_talao(request.user),
        'gerencia_vale': combustivel_gerencia_vale(request.user),
        'beneficiario': combustivel_beneficiario(request.user),
    }

    return render(request, 'web_gc/menu_consultas.html', context)


@login_required()
def view_menu_relatorios(request):
    """
    View de carregamento da página de relatórios do GC
    :param request: informações gerais
    :return: carregamento da página de relatórios
    """

    context = {
        'gerencia_talao': combustivel_gerencia_talao(request.user),
        'gerencia_vale': combustivel_gerencia_vale(request.user),
        'beneficiario': combustivel_beneficiario(request.user),
    }

    return render(request, 'web_gc/menu_relatorios.html', context)


@login_required()
def view_menu_taloes(request):
    """
    View de carregamento da página de gerenciamento de talões do GC
    :param request: informações gerais
    :return: carregamento da página de gerenciamento de talões
    """

    context = {
        'gerencia_talao': combustivel_gerencia_talao(request.user),
        'gerencia_vale': combustivel_gerencia_vale(request.user),
        'beneficiario': combustivel_beneficiario(request.user),
    }

    return render(request, 'web_gc/menu_taloes.html', context)


@login_required()
def view_menu_vales(request):
    """
    View de carregamento da página de gerenciamento de vales do GC
    :param request: informações gerais
    :return: carregamento da página de gerenciamento de vales
    """

    context = {
        'gerencia_talao': combustivel_gerencia_talao(request.user),
        'gerencia_vale': combustivel_gerencia_vale(request.user),
        'beneficiario': combustivel_beneficiario(request.user),
    }

    return render(request, 'web_gc/menu_vales.html', context)


@login_required()
@permission_required(
    (
        'web_gc.view_talao',
    ),
    raise_exception=True)
def view_taloes(request):
    """
    View de exibição dos talões cadastrados no sistema
    :param request: informações gerais
    :return: lista de talões cadastrados
    """

    taloes = Talao.objects.all()
    context = {
        'taloes': taloes
    }

    return render(request, 'web_gc/consulta_talao.html', context)


@login_required()
@permission_required(
    (
        'web_gc.view_talao',
        'web_gc.view_vale',
    ),
    raise_exception=True)
def view_talao(request, **kwargs):
    """
    View de exibição de informações de talão
    :param request: informações gerais
    :param kwargs: id do talão desejado
    :return: informações do talão requerido
    """

    talao = get_object_or_404(Talao, talao=kwargs.get('talao_id'))
    context = {
        'talao': talao,
    }
    return render(request, 'web_gc/detalhes_talao.html', context)


@login_required()
@permission_required(
    (
        'web_gc.view_talao',
        'web_gc.view_vale',
    ),
    raise_exception=True)
def view_vales(request):
    """

    :param request:
    :return:
    """

    vales = Vale.objects.all().order_by('vale_entrega__data')
    context = {
        'vales': vales,
    }

    return render(request, 'web_gc/consulta_vales.html', context)


@login_required()
@permission_required(
    (
        'web_gc.view_vale',
    ),
    raise_exception=True)
def view_meus_vales(request):
    """

    :param request:
    :return:
    """

    vales = Vale.objects.filter(vale_entrega__user_to=request.user).order_by('vale_entrega__data')
    context = {
        'vales': vales,
    }
    print(vales)

    return render(request, 'web_gc/consulta_meus_vales.html', context)


def view_relatorio_mensal(request):
    """

    :param request:
    :return:
    """

    vales = Vale.objects.values('vale_entrega__user_to__username').annotate(total=Sum('vale_entrega__valor'))
    context = {
        'vales': vales,
    }

    return render(request, 'web_gc/relatorio_mensal.html', context)


def view_form_teste(request):

    if request.method == 'POST':
        form = FormTest(request.POST)

        if form.is_valid():
            data = User.objects.all()
            print(data)
            context = {
                'users': data,
            }

            return render(request, 'web_gc/teste1.html', context)

    else:
        form = FormTest()

        return render(request, 'web_gc/teste.html', {'form': form})
