from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q, Max
from django.core.paginator import Paginator

from .forms import *
from .models import Secao, Modelo
from .menu import menu_principal, menu_cadastros, menu_consultas

from constel.objects import Button
from constel.apps.controle_acessos.decorator import permission
from constel.forms import FormFuncionario


@login_required()
@permission('almoxarifado', )
def index(request):
    context = menu_principal(request)

    return render(request, 'constel/v2/app.html', context)


@login_required()
@permission('almoxarifado', )
def cadastros(request):
    context = menu_cadastros(request)

    return render(request, 'constel/v2/app.html', context)


@login_required()
@permission('almoxarifado', )
def cadastrar_secao(request):
    menu = menu_cadastros(request)

    if request.method == 'POST':
        form = FormCadastraSecao(request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/almoxarifado/cont/menu-cadastros/')
    else:
        form = FormCadastraSecao()

    itens = Secao.objects.all().values(
        'nome',
        'descricao',
        'data',
    ).order_by('nome', 'descricao')

    paginator = Paginator(itens, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form': form,
        'form_submit_text': 'Cadastrar seção',
    }
    context.update(menu)

    return render(request, 'cont/v2/cadastra_secao.html', context)


@login_required()
@permission('almoxarifado', )
def cadastrar_modelo(request):
    menu = menu_cadastros(request)

    if request.method == 'POST':
        form = FormCadastraModelo(request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/almoxarifado/cont/menu-cadastros/')
    else:
        form = FormCadastraModelo()

    itens = Modelo.objects.all().values(
        'nome',
        'descricao',
        'data',
    ).order_by('nome', 'descricao')

    paginator = Paginator(itens, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form': form,
        'form_submit_text': 'Cadastrar modelo',
    }
    context.update(menu)

    return render(request, 'cont/v2/cadastra_modelo.html', context)


@login_required()
@permission('almoxarifado', )
def entrada_1(request):
    menu = menu_principal(request)

    if request.method == 'POST':
        initial = {
            'modelo': request.session.get('cont2_entrada_modelo', None),
            'secao': request.session.get('cont2_entrada_secao', None),
        }
        form = FormEntradaOnt1(data=request.POST, initial=initial)

        if form.is_valid():
            request.session['cont2_entrada_modelo'] = form.cleaned_data['modelo']
            request.session['cont2_entrada_secao'] = form.cleaned_data['secao']

            return HttpResponseRedirect('/almoxarifado/cont/entrada-2')
    else:
        form = FormEntradaOnt1()

    context = {
        'form': form,
        'form_submit_text': 'Avançar',
    }
    context.update(menu)

    return render(request, 'cont/v2/entrada_1.html', context)


@login_required()
@permission('almoxarifado', )
def entrada_2(request):
    menu = menu_principal(request)

    if request.session.get('cont2_entrada_modelo') is None or request.session.get('cont2_entrada_secao') is None:

        return HttpResponseRedirect('/almoxarifado/cont/entrada-1/')

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

            return HttpResponseRedirect('/almoxarifado/cont/entrada-2/')

    else:
        form = FormEntradaOnt2()

    historico = OntEntradaHistorico.objects.filter(user=request.user).order_by('id').values(
        'ont__codigo',
    )

    context = {
        'form': form,
        'form_submit_text': 'Inserir',
        'callback': 'almoxarifado_cont_entrada_ont_3',
        'modelo': modelo.nome,
        'secao': secao.nome,
        'historico': historico,
    }
    context.update(menu)

    return render(request, 'cont/v2/entrada_2.html', context)


@login_required()
@permission('almoxarifado', )
def entrada_3(request):

    OntEntradaHistorico.objects.filter(user=request.user).delete()
    request.session.pop('cont2_entrada_modelo')
    request.session.pop('cont2_entrada_secao')

    return HttpResponseRedirect('/almoxarifado/cont/entrada-1')


@login_required()
@permission('almoxarifado', )
def consultas(request):
    context = menu_consultas(request)

    return render(request, 'constel/v2/app.html', context)


@login_required()
@permission('almoxarifado', )
def consulta_status(request):
    menu = menu_consultas(request)

    onts = Ont.objects.all()

    onts_qtde = onts.aggregate(Count('codigo'))

    onts_status_secao_modelo = onts.values(
        'status',
        'secao__nome',
        'modelo__nome',
        'secao__id',
        'modelo__id',
    ).annotate(
        Count('codigo')
    ).order_by(
        'status',
        'secao__nome',
        'modelo__nome',
    )

    context = {
        'onts_status_secao_modelo': onts_status_secao_modelo,
    }
    context.update(menu)

    return render(request, 'cont/v2/consulta_status.html', context)


@login_required()
@permission('almoxarifado', )
def consulta_status_detalhe(request, status, secao, modelo):
    menu = menu_consultas(request)

    itens = Ont.objects.filter(
        status=status,
        secao__id=secao,
        modelo__id=modelo,
    ).values(
        'codigo',
    ).annotate(
        max_data=Max('entrada_ont__data')
    ).order_by(
        'max_data',
    )
    
    paginator = Paginator(itens, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    context.update(menu)

    return render(request, 'cont/v2/consulta_status_detalhe.html', context)


@login_required()
@permission('almoxarifado', )
def consulta_tecnicos_carga(request):
    menu = menu_consultas(request)

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

    itens = cargas.values(
        'username',
        'first_name',
        'last_name',
        'max_data',
        'total',
    ).exclude(total=0)

    paginator = Paginator(itens, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form_submit_text': 'Filtrar',
        'form': form,
    }
    context.update(menu)

    return render(request, 'cont/v2/consulta_tecnicos_carga.html', context)


@login_required()
@permission('almoxarifado', )
def consulta_tecnicos_carga_detalhe(request, funcionario):
    menu = menu_consultas(request)

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

    funcionario = User.objects.get(username=funcionario)

    funcionario = {
        'first_name': funcionario.first_name,
        'last_name': funcionario.last_name,
    }

    paginator = Paginator(carga, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'funcionario': funcionario,
    }
    context.update(menu)

    return render(request, 'cont/v2/consulta_tecnicos_carga_detalhe.html', context)


@login_required()
@permission('almoxarifado', )
def view_dashboard(request):
    pass
