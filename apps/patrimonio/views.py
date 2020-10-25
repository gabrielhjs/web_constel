from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from constel.apps.controle_acessos.decorator import permission

from .menu import menu_principal, menu_cadastros, menu_entradas, menu_saidas, menu_consultas, menu_consultas_modelos


@login_required
@permission('patrimonio', )
def view_menu_relatorios(request):

    return render(request, 'patrimonio/menu_relatorios.html')


@login_required
@permission('patrimonio', )
def index(request):

    context = menu_principal(request)

    return render(request, 'constel/v2/app.html', context)


@login_required
@permission('patrimonio', )
def cadastros(request):
    context = menu_cadastros(request)

    return render(request, 'constel/v2/app.html', context)


@login_required
@permission('patrimonio', )
def entradas(request):
    context = menu_entradas(request)

    return render(request, 'constel/v2/app.html', context)


@login_required
@permission('patrimonio', )
def saidas(request):
    context = menu_saidas(request)

    return render(request, 'constel/v2/app.html', context)


@login_required
@permission('patrimonio', )
def consultas(request):
    context = menu_consultas(request)

    return render(request, 'constel/v2/app.html', context)


@login_required
@permission('patrimonio', )
def consultas_modelos(request):
    context = menu_consultas_modelos(request)

    return render(request, 'constel/v2/app.html', context)
