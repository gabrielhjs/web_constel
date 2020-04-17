from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q, Max

from .forms import *
from .models import Secao, Modelo

from constel.objects import Button
from constel.apps.controle_acessos.decorator import permission
from constel.forms import FormFuncionario


@login_required()
@permission('almoxarifado', )
def view_menu_principal(request):

    button_1 = Button('almoxarifado_cont_entrada_ont_1', 'Entrada de ONT\'s')
    button_2 = Button('almoxarifado_cont_saida_lista', 'Saída de ONT\'s')
    button_3 = Button('almoxarifado_cont_menu_cadastros', 'Cadastros')
    button_4 = Button('almoxarifado_cont_menu_consultas', 'Consultas')
    # button_5 = Button('almoxarifado_cont_menu_relatorios', 'Relatórios')
    button_voltar = Button('almoxarifado_menu_principal', 'Voltar')

    context = {
        'guia_titulo': 'Constel | Cont2',
        'pagina_titulo': 'Cont2',
        'menu_titulo': 'Menu principal',
        'buttons': [
            button_1,
            button_2,
            button_3,
            button_4,
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
    button_voltar = Button('almoxarifado_cont_menu_principal', 'Voltar')

    context = {
        'guia_titulo': 'Constel | Cont2',
        'pagina_titulo': 'Cont2',
        'menu_titulo': 'Menu de cadastros',
        'buttons': [
            button_1,
            button_2,
        ],
        'rollback': button_voltar,
    }

    return render(request, 'constel/menu.html', context)


@login_required()
@permission('almoxarifado', )
def view_menu_consultas(request):

    button_1 = Button('almoxarifado_cont_consulta_situacao', 'Situação atual')
    button_2 = Button('almoxarifado_cont_consulta_tecnicos_carga', 'Cargas de ONT\'s')
    button_voltar = Button('almoxarifado_cont_menu_principal', 'Voltar')

    context = {
        'guia_titulo': 'Constel | Cont2',
        'pagina_titulo': 'Cont2',
        'menu_titulo': 'Menu de consultas',
        'buttons': [
            button_1,
            button_2,
        ],
        'rollback': button_voltar,
    }

    return render(request, 'constel/menu.html', context)


@login_required()
@permission('almoxarifado', )
def view_consulta_situacao(request):

    onts = Ont.objects.all()

    onts_qtde = onts.aggregate(Count('codigo'))

    onts_status = onts.values(
        'status',
    ).annotate(
        Count('codigo')
    ).order_by(
        'status',
    )

    onts_status_secao = onts.values(
        'status',
        'secao__nome',
    ).annotate(
        Count('codigo')
    ).order_by(
        'status',
        'secao__nome',
    )

    onts_status_secao_modelo = onts.values(
        'status',
        'secao__nome',
        'modelo__nome',
    ).annotate(
        Count('codigo')
    ).order_by(
        'status',
        'secao__nome',
        'modelo__nome',
    )

    rowspan = {
        'secao': len(onts_status_secao_modelo),
        'status': len(onts_status_secao_modelo) * len(onts_status_secao),
    }

    context = {
        'pagina_titulo': 'Situação',
        'onts_total': onts_qtde,
        'onts_status': onts_status,
        'onts_status_secao': onts_status_secao,
        'onts_status_secao_modelo': onts_status_secao_modelo,
        'rowspan': rowspan,
    }

    return render(request, 'cont/consulta_situacao.html', context)


@login_required()
@permission('almoxarifado', )
def view_consulta_tecnicos_carga(request):

    funcionario = request.GET.get('funcionario', '')

    form = FormFuncionario(initial={'funcionario': funcionario})

    query = Q()

    if funcionario != '':
        query = query & Q(
            Q(username__icontains=funcionario) |
            Q(first_name__icontains=funcionario) |
            Q(last_name__icontains=funcionario))

    cargas = User.objects.filter(query).annotate(
        total=Count('saida_user_to__ont', filter=Q(saida_user_to__ont__status=1), distinct=True),
        max_data=Max('saida_user_to__data', filter=Q(saida_user_to__ont__status=1)),
    ).order_by(
        '-total',
    )

    cargas = cargas.values(
        'username',
        'first_name',
        'last_name',
        'max_data',
        'total',
    ).exclude(total=0)

    context = {
        'pagina_titulo': 'Consulta de carga de ONT\'s',
        'button_submit_text': 'Filtrar',
        'form': form,
        'cargas': cargas,
    }

    return render(request, 'cont/consulta_tecnicos_carga.html', context)


@login_required()
@permission('almoxarifado', )
def view_consulta_tecnicos_carga_detalhe(request, funcionario):

    carga = OntSaida.objects.values(
        'ont__codigo',
        'user__first_name',
        'user__last_name',
        'user_to__first_name',
        'user_to__last_name',
    ).annotate(
        max_data=Max('data')
    ).filter(
        ont__status=1,
        user_to__username=funcionario,
    ).order_by(
        '-max_data'
    )

    print(carga)

    context = {
        'button_submit_text': 'Filtrar',
        'carga': carga,
        'funcionario': funcionario,
    }

    return render(request, 'cont/consulta_tecnicos_carga_detalhes.html', context)


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

                messages.success(request, 'Ont (RE)inserida no estoque com sucesso!')

            else:
                ont = Ont(
                    codigo=serial,
                    status=0,
                    modelo=modelo,
                    secao=secao,
                )
                ont.save()

                messages.success(request, 'Ont cadastrada e inserida no estoque com sucesso!')

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
