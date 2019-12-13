from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .permissions import *


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
