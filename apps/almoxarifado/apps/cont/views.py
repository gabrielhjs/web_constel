from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .forms import *
from .models import Secao, Modelo

from constel.objects import Button
from constel.models import UserType
from constel.apps.controle_acessos.decorator import permission


@login_required()
@permission('almoxarifado', )
def view_menu_principal(request):

    button_1 = Button('almoxarifado_cont_menu_cadastros', 'Cadastros')
    button_2 = Button('almoxarifado_cont_entrada_ont', 'Entrada de ONT')
    button_3 = Button('cont_menu_saidas', 'Saídas')
    button_4 = Button('cont_menu_consultas', 'Consultas')
    button_5 = Button('cont_menu_relatorios', 'Relatórios')
    button_voltar = Button('almoxarifado_menu_principal', 'Voltar')

    context = {
        'guia_titulo': 'Constel | Cont 2',
        'pagina_titulo': 'Cont 2',
        'menu_titulo': 'Menu principal',
        'buttons': [
            button_1,
            # button_2,
            # button_3,
            # button_4,
            # button_5,
        ],
        'rollback': button_voltar,
    }

    return render(request, 'constel/menu.html', context)


@login_required()
@permission('almoxarifado', )
def view_menu_cadastros(request):

    button_1 = Button('almoxarifado_cont_cadastrar_secao', 'Cadastrar seção de ONT')
    button_2 = Button('almoxarifado_cont_cadastrar_modelo', 'Cadastrar modelo de ONT')
    button_3 = Button('cont_menu_saidas', 'Saídas')
    button_4 = Button('cont_menu_consultas', 'Consultas')
    button_5 = Button('cont_menu_relatorios', 'Relatórios')
    button_voltar = Button('almoxarifado_cont_menu_principal', 'Voltar')

    context = {
        'guia_titulo': 'Constel | Cont 2',
        'pagina_titulo': 'Cont 2',
        'menu_titulo': 'Menu principal',
        'buttons': [
            button_1,
            button_2,
            # button_3,
            # button_4,
            # button_5,
        ],
        'rollback': button_voltar,
    }

    return render(request, 'constel/menu.html', context)


@login_required()
@permission('almoxarifado', )
def view_cadastrar_secao(request):

    if request.method == 'POST':
        form = FormCadastraSecao(request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/almoxarifado/cont/menu-cadastros/')
    else:
        form = FormCadastraSecao()

    secoes = Secao.objects.all().order_by('nome', 'descricao')
    secoes = secoes.values(
        'nome',
        'descricao',
    )

    context = {
        'secoes': secoes,
        'form': form,
        'button_submit_text': 'Cadastrar seção',
        'callback': 'almoxarifado_cont_menu_cadastros',
        'callback_text': 'Cancelar',
        'pagina_titulo': 'Cont 2',
        'menu_titulo': 'Cadastro de seção de ONT',
    }

    return render(request, 'cont/cadastrar_secao.html', context)


@login_required()
@permission('almoxarifado', )
def view_cadastrar_modelo(request):

    if request.method == 'POST':
        form = FormCadastraModelo(request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/almoxarifado/cont/menu-cadastros/')
    else:
        form = FormCadastraModelo()

    modelos = Modelo.objects.all().order_by('nome', 'descricao')
    modelos = modelos.values(
        'nome',
        'descricao',
    )

    context = {
        'modelos': modelos,
        'form': form,
        'button_submit_text': 'Cadastrar modelo',
        'callback': 'almoxarifado_cont_menu_cadastros',
        'callback_text': 'Cancelar',
        'pagina_titulo': 'Cont 2',
        'menu_titulo': 'Cadastro de modelos de ONT',
    }

    return render(request, 'cont/cadastrar_modelo.html', context)
