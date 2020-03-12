from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
    button_2 = Button('almoxarifado_cont_entrada_ont_1', 'Entrada de ONT\'s')
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


@login_required()
@permission('almoxarifado', )
def view_entrada_ont_1(request):

    if request.method == 'POST':
        initial = {
            'modelo': request.session.get('cont2_entrada_modelo', None),
            'secao': request.session.get('cont2_entrada_secao', None),
        }
        form = FormEntradaOnt1(data=request.POST, initial=initial)

        if form.is_valid():
            request.session['cont2_entrada_modelo'] = form.cleaned_data['modelo']
            request.session['cont2_entrada_secao'] = form.cleaned_data['secao']

            return HttpResponseRedirect('/almoxarifado/cont/entrada-ont-2/')
    else:
        form = FormEntradaOnt1()

    context = {
        'form': form,
        'button_submit_text': 'Avançar',
        'callback': 'almoxarifado_cont_menu_principal',
        'callback_text': 'Cancelar',
        'pagina_titulo': 'Cont 2',
        'menu_titulo': 'Entrada de ONT\'s',
    }

    return render(request, 'cont/entrada_ont_1.html', context)


@login_required()
@permission('almoxarifado', )
def view_entrada_ont_2(request):

    if request.session.get('cont2_entrada_modelo') is None or request.session.get('cont2_entrada_secao') is None:

        return HttpResponseRedirect('/almoxarifado/cont/entrada-ont-1/')

    modelo = Modelo.objects.get(id=request.session['cont2_entrada_modelo'])
    secao = Secao.objects.get(id=request.session['cont2_entrada_secao'])

    if request.method == 'POST':
        form = FormEntradaOnt2(request.POST)

        if form.is_valid():
            serial = form.cleaned_data['serial'].upper()
            if Ont.objects.filter(codigo=serial).exists():
                ont = Ont.objects.get(codigo=serial)
                ont.status = 0
                ont.save()

                messages.success(request, 'Serial (RE)inserido no estoque com sucesso!')

            else:
                ont = Ont(
                    codigo=serial,
                    status=0,
                    modelo=modelo,
                    secao=secao,
                )
                ont.save()

                messages.success(request, 'Serial cadastrado e inserido no estoque com sucesso!')

            OntEntrada(ont=ont, user=request.user).save()
            OntEntradaHistorico(ont=ont, user=request.user).save()

            return HttpResponseRedirect('/almoxarifado/cont/entrada-ont-2/')

    else:
        form = FormEntradaOnt2()

    historico = OntEntradaHistorico.objects.filter(user=request.user).order_by('id').values(
        'ont__codigo',
    )

    context = {
        'form': form,
        'button_submit_text': 'Inserir',
        'callback': 'almoxarifado_cont_entrada_ont_3',
        'callback_text': 'Concluir',
        'pagina_titulo': 'Cont 2',
        'menu_titulo': 'Entrada de ONT\'s',
        'modelo': modelo.nome,
        'secao': secao.nome,
        'historico': historico,
    }

    return render(request, 'cont/entrada_ont_2.html', context)


@login_required()
@permission('almoxarifado', )
def view_entrada_ont_3(request):

    OntEntradaHistorico.objects.filter(user=request.user).delete()
    request.session.pop('cont2_entrada_modelo')
    request.session.pop('cont2_entrada_secao')

    return HttpResponseRedirect('/almoxarifado/cont/entrada-ont-1/')
