import datetime

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.db.models import (
    Count,
    Max,
    Min,
    Q,
    Sum,
    OuterRef,
    Subquery,
    F,
    IntegerField,
    ExpressionWrapper,
    DecimalField
)
from django.db.models.functions import TruncMonth, Coalesce, TruncDay
from django.http import HttpResponseRedirect
from django.shortcuts import render

from constel.apps.controle_acessos.decorator import permission
from constel.forms import (
    FormDataInicialFinal,
    FormDataInicialFinalFuncionario,
    FormFiltraQData,
    FormFiltraQ
)
from constel.models import UserType

from .forms import *
from .menu import menu_cadastros, menu_consultas, menu_principal, menu_edicao
from .models import Material, Fornecedor, MaterialEntrada, MaterialFornecedorPrazo


@login_required()
@permission('almoxarifado', )
def index(request):
    menu = menu_principal(request)

    almoxarifado = MaterialSaida.objects.filter(
        material__codigo__in=[20014434, 20010213, 15022859, 15018751]
    ).annotate(
        mes=TruncMonth('data')
    ).values(
        'mes',
    ).annotate(
        total_1=Coalesce(Sum('quantidade', filter=Q(material__codigo=20014434)), 0),
        total_2=Coalesce(Sum('quantidade', filter=Q(material__codigo=20010213)), 0),
        total_3=Coalesce(Sum('quantidade', filter=Q(material__codigo=15022859)), 0),
        total_4=Coalesce(Sum('quantidade', filter=Q(material__codigo=15018751)), 0),
    ).order_by(
        'mes'
    )

    hoje = datetime.datetime.today()

    cabos_mes = MaterialSaida.objects.filter(
        material__codigo__in=[20014434, 20010213],
        data__year=hoje.year,
        data__month=hoje.month,
    ).annotate(
        dia=TruncDay('data')
    ).values(
        'dia',
    ).annotate(
        total_1=Coalesce(Sum('quantidade', filter=Q(material__codigo=20014434)), 0),
        total_2=Coalesce(Sum('quantidade', filter=Q(material__codigo=20010213)), 0),
    ).order_by(
        'dia'
    )

    conector_protetor_cumulativo = MaterialSaida.objects.filter(
        material__codigo__in=[15022859, 15018751],
        data__day__lte=hoje.day,
    ).annotate(
        mes=TruncMonth('data')
    ).values(
        'mes',
    ).annotate(
        total_1=Coalesce(Sum('quantidade', filter=Q(material__codigo=15022859)), 0),
        total_2=Coalesce(Sum('quantidade', filter=Q(material__codigo=15018751)), 0),
    ).order_by(
        'mes'
    )

    context = {
        'almoxarifado': almoxarifado,
        'cabos_mes': cabos_mes,
        'conector_protetor_cumulativo': conector_protetor_cumulativo,
    }
    context.update(menu)

    return render(request, 'almoxarifado/v2/dashboard.html', context)


@login_required()
@permission('almoxarifado', )
def cadastros(request):
    context = menu_cadastros(request)

    return render(request, 'constel/v2/app.html', context)


@login_required()
@permission('almoxarifado', )
def cadastra_material(request):
    menu = menu_cadastros(request)

    if request.method == 'POST':
        form = FormCadastraMaterial(request.POST)

        if form.is_valid():
            material = Material(
                codigo=form.cleaned_data['codigo'],
                material=form.cleaned_data['material'],
                descricao=form.cleaned_data['descricao'],
                user=request.user,
            )
            material.save()
            MaterialQuantidade(
                material=material,
                quantidade=0,
            ).save()

            return HttpResponseRedirect('/almoxarifado/cadastros/material/')
    else:
        form = FormCadastraMaterial()

    itens = Material.objects.values(
        'codigo',
        'material',
        'descricao',
        'data',
        'user__first_name',
        'user__last_name',
    )

    paginator = Paginator(itens, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form': form,
        'form_submit_text': 'Cadastrar novo material',
    }
    context.update(menu)

    return render(request, 'almoxarifado/v2/cadastra_material.html', context)


@login_required()
@permission('almoxarifado', 'gestor', )
def cadastra_fornecedor(request):
    menu = menu_cadastros(request)

    if request.method == 'POST':
        form = FormCadastraFornecedor(request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/almoxarifado/cadastros/fornecedor/')
    else:
        form = FormCadastraFornecedor()

    itens = Fornecedor.objects.values(
        'nome',
        'cnpj',
    ).order_by('nome', 'cnpj')

    paginator = Paginator(itens, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form': form,
        'form_submit_text': 'Cadastrar novo fornecedor',
    }
    context.update(menu)

    return render(request, 'almoxarifado/v2/cadastra_fornecedor.html', context)


@login_required()
@permission('almoxarifado', )
def edicao(request):
    context = menu_edicao(request)

    return render(request, 'constel/v2/app.html', context)


@login_required()
@permission('almoxarifado', )
def edicao_material(request):
    menu = menu_edicao(request)

    material = request.GET.get('q', '')

    form = FormFiltraQ(
        descricao='nome ou código',
        initial={
            'q': material
        }
    )

    query = Q()

    if material != '':
        query = query & Q(
            Q(codigo__icontains=material) |
            Q(material__icontains=material)
        )

    itens = Material.objects.filter(
        query
    ).values(
        'codigo',
        'material',
        'descricao',
        'data',
        'user__first_name',
        'user__last_name',
        'status',
    ).order_by(
        'material'
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

    return render(request, 'almoxarifado/v2/edicao_material.html', context)


@login_required()
@permission('almoxarifado', )
def edicao_material_edita(request, material):
    menu = menu_edicao(request)

    material = get_object_or_404(Material, codigo=material)

    form = FormMaterialEdita(request.POST or None, instance=material)

    if form.is_valid():
        form.save()

        return HttpResponseRedirect('/almoxarifado/edicao/material/?' + request.GET.urlencode())

    itens = MaterialFornecedorPrazo.objects.filter(
        material=material
    ).values(
        'fornecedor__nome',
        'dias',
        'dias_uteis',
    )

    paginator = Paginator(itens, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form': form,
        'form_submit_text': 'Salvar',
        'material_codigo': material.codigo
    }
    context.update(menu)

    return render(request, 'almoxarifado/v2/edicao_material_edita.html', context)


def edicao_material_fornecedor_prazo(request, material):
    menu = menu_edicao(request)

    material = get_object_or_404(Material, codigo=material)

    form = FormMaterialFornecedorPrazo(request.POST or None)

    if form.is_valid():
        MaterialFornecedorPrazo(
            material=material,
            fornecedor=form.cleaned_data['fornecedor'],
            dias=form.cleaned_data['dias'],
            dias_uteis=form.cleaned_data['dias_uteis'],
        ).save()

        return HttpResponseRedirect('/almoxarifado/edicao/material/'+str(material.codigo)+'/?'+request.GET.urlencode())

    context = {
        'form': form,
        'form_submit_text': 'Cadastrar prazo',
        'material_codigo': material.codigo,
    }
    context.update(menu)

    return render(request, 'almoxarifado/v2/edicao_material_fornecedor_prazo.html', context)


@login_required()
@permission('almoxarifado', 'almoxarifado - entrada', )
def entrada_material(request):
    menu = menu_principal(request)

    if request.method == 'POST':
        form = FormEntradaMaterial(request.POST)

        if form.is_valid():
            ordem = Ordem.objects.create(tipo=0, user=request.user)
            ordem.save()
            entrada = MaterialEntrada(
                material=form.cleaned_data['material'],
                quantidade=form.cleaned_data['quantidade'],
                observacao=form.cleaned_data['observacao'],
                fornecedor=form.cleaned_data['fornecedor'],
                user=request.user,
                ordem=ordem,
            )
            material = form.cleaned_data['material']
            material.quantidade.quantidade += form.cleaned_data['quantidade']

            entrada.save()
            material.quantidade.save()

            return HttpResponseRedirect('/almoxarifado/')

    else:
        form = FormEntradaMaterial()

    context = {
        'form': form,
        'form_submit_text': 'Registrar entrada',
    }
    context.update(menu)

    return render(request, 'almoxarifado/v2/entrada.html', context)


def consultas(request):
    menu = menu_consultas(request)

    return render(request, 'constel/v2/app.html', context=menu)


@login_required()
@permission('almoxarifado', )
def consulta_estoque(request):
    menu = menu_consultas(request)

    material = request.GET.get('material', '')

    form = FormMaterial(
        initial={
            'material': material,
        }
    )

    query = Q()

    if material != '':
        query = query & Q(
            Q(codigo__icontains=material) |
            Q(material__icontains=material)
        )

    data_fim = datetime.datetime.now()
    data_intervalo = 30
    data_inicio = data_fim - datetime.timedelta(days=data_intervalo)

    subquery1 = MaterialSaida.objects.filter(
        material=OuterRef('pk'),
        data__gte=data_inicio
    ).values(
        'material__material'
    ).annotate(
        total=ExpressionWrapper(Sum(F('quantidade')), output_field=DecimalField())
    ).values(
        'total'
    )

    itens = Material.objects.filter(
        query,
    ).values(
        'codigo',
        'material',
        'quantidade__quantidade',
    ).annotate(
        total=Subquery(subquery1)
    ).annotate(
        pt=ExpressionWrapper(
            F('quantidade__quantidade') * float(data_intervalo) / F('total'),
            output_field=IntegerField()
        )
    ).annotate(
        pt_min=ExpressionWrapper(F('pt') - Max('almoxarifado_material_prazo__dias'), output_field=IntegerField()),
        pt_max=ExpressionWrapper(F('pt') - Min('almoxarifado_material_prazo__dias'), output_field=IntegerField()),
    ).exclude(
        entradas__isnull=True,
    ).order_by('material')

    paginator = Paginator(itens, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form': form,
        'form_submit_text': 'Filtrar',
    }
    context.update(menu)

    return render(request, 'almoxarifado/v2/consulta_estoque.html', context)


def consulta_estoque_prazo_fornecedor(request, material):
    menu = menu_consultas(request)

    material = get_object_or_404(Material, codigo=material)

    itens = MaterialFornecedorPrazo.objects.filter(
        material=material
    ).values(
        'fornecedor__nome',
        'dias',
        'dias_uteis',
    )

    paginator = Paginator(itens, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    context.update(menu)

    return render(request, 'almoxarifado/v2/consulta_estoque_fornecedor_prazo.html', context)


def consulta_estoque_detalhe(request, material):
    menu = menu_consultas(request)

    def daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + datetime.timedelta(n)

    entradas = MaterialEntrada.objects.filter(material__codigo=material).values('quantidade', 'data')
    saidas = MaterialSaida.objects.filter(material__codigo=material).values('quantidade', 'data')

    data_inicial = entradas[0]['data'].date()
    data_final = datetime.datetime.today().date()
    saldos = []
    saldo_dia = 0

    for dia in daterange(data_inicial, data_final + datetime.timedelta(days=1)):

        for dia_entrada in entradas:

            if dia_entrada['data'].date() == dia:
                saldo_dia += dia_entrada['quantidade']

        for dia_saida in saidas:

            if dia_saida['data'].date() == dia:
                saldo_dia -= dia_saida['quantidade']

        saldos.append({'dia': dia, 'saldo': saldo_dia})

    context = {
        'saldos': saldos,
        'material': Material.objects.get(codigo=material),
    }
    context.update(menu)

    return render(request, 'almoxarifado/v2/consulta_estoque_detalhe.html', context)


@login_required()
@permission('almoxarifado', )
def consulta_ordem_entrada(request):
    menu = menu_consultas(request)

    data_inicial = request.GET.get('data_inicial', '')
    data_final = request.GET.get('data_final', '')

    form = FormDataInicialFinal(
        initial={
            'data_inicial': data_inicial,
            'data_final': data_final,
        }
    )

    query = Q(tipo=0)

    if data_inicial != '':
        data_inicial = datetime.datetime.strptime(data_inicial, "%Y-%m-%d").date()
        query = query & Q(data__gte=data_inicial)

    if data_final != '':
        data_final = datetime.datetime.strptime(data_final, "%Y-%m-%d").date()
        query = query & Q(data__lte=data_final)

    itens = Ordem.objects.filter(query).order_by(
        '-data'
    ).annotate(
        user_to_first_name=Min('almoxarifado_ordem_saida__user_to__first_name'),
        user_to_last_name=Min('almoxarifado_ordem_saida__user_to__last_name'),
    )
    itens = itens.values(
        'id',
        'data',
        'user__first_name',
        'user__last_name',
        'user_to_first_name',
        'user_to_last_name',
    )
    paginator = Paginator(itens, 50)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'tipo': 0,
        'form': form,
        'form_submit_text': 'filtrar'
    }
    context.update(menu)

    return render(request, 'almoxarifado/v2/consulta_ordem.html', context)


@login_required()
@permission('almoxarifado', )
def consulta_ordem_saida(request):
    menu = menu_consultas(request)

    data_inicial = request.GET.get('data_inicial', '')
    data_final = request.GET.get('data_final', '')

    form = FormDataInicialFinal(
        initial={
            'data_inicial': data_inicial,
            'data_final': data_final,
        }
    )

    query = Q(tipo=1, almoxarifado_ordem_saida__id__gte=0)

    if data_inicial != '':
        data_inicial = datetime.datetime.strptime(data_inicial, "%Y-%m-%d").date()
        query = query & Q(data__gte=data_inicial)

    if data_final != '':
        data_final = datetime.datetime.strptime(data_final, "%Y-%m-%d").date()
        query = query & Q(data__lte=data_final)

    itens = Ordem.objects.filter(query).order_by(
        '-data'
    ).annotate(
        user_to_first_name=Min('almoxarifado_ordem_saida__user_to__first_name'),
        user_to_last_name=Min('almoxarifado_ordem_saida__user_to__last_name'),
    ).values(
        'id',
        'data',
        'user__first_name',
        'user__last_name',
        'user_to_first_name',
        'user_to_last_name',
    )
    paginator = Paginator(itens, 50)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'tipo': 1,
        'form': form,
        'form_submit_text': 'filtar',
    }
    context.update(menu)

    return render(request, 'almoxarifado/v2/consulta_ordem.html', context)


@login_required()
@permission('almoxarifado', )
def consulta_ordem_detalhe(request, **kwargs):

    if Ordem.objects.filter(id=kwargs.get('ordem')).exists():
        menu = menu_consultas(request)
        ordem = Ordem.objects.get(id=kwargs.get('ordem'))

        if kwargs.get('tipo'):
            itens = MaterialSaida.objects.filter(ordem=ordem).order_by('material__material', 'material__codigo')

        else:
            itens = MaterialEntrada.objects.filter(ordem=ordem).order_by('material__material', 'material__codigo')

        itens = itens.values(
            'material__codigo',
            'material__material',
            'quantidade',
        )
        paginator = Paginator(itens, 50)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'page_obj': page_obj,
            'ordem': ordem,
            'tipo': kwargs.get('tipo'),
        }
        context.update(menu)

        return render(request, 'almoxarifado/v2/consulta_ordem_detalhe.html', context)

    else:

        return HttpResponseRedirect('/almoxarifado/consultas/')


@login_required()
@permission('almoxarifado', 'gestor', )
def consulta_funcionario(request):
    menu = menu_consultas(request)

    data_inicial = request.GET.get('data_inicial', '')
    data_final = request.GET.get('data_final', '')
    funcionario = request.GET.get('funcionario', '')

    form = FormDataInicialFinalFuncionario(
        initial={
            'data_inicial': data_inicial,
            'data_final': data_final,
            'funcionario': funcionario,
        }
    )

    query = Q()

    if funcionario != '':
        query = query & Q(
            Q(username__icontains=funcionario) |
            Q(first_name__icontains=funcionario) |
            Q(last_name__icontains=funcionario))

    if data_inicial != '':
        data_inicial = datetime.datetime.strptime(data_inicial, "%Y-%m-%d").date()
        query = query & Q(almoxarifado_retiradas__data__gte=data_inicial)

    if data_final != '':
        data_final = datetime.datetime.strptime(data_final, "%Y-%m-%d").date()
        query = query & Q(almoxarifado_retiradas__data__lte=data_final)

    retiradas = User.objects.filter(query).annotate(
        total=Count('almoxarifado_retiradas__ordem__id', distinct=True),
        max_data=Max('almoxarifado_retiradas__data'),
    ).order_by(
        '-total'
    )

    retiradas = retiradas.values(
        'username',
        'first_name',
        'last_name',
        'max_data',
        'total',
    ).exclude(total=0)

    paginator = Paginator(retiradas, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form': form,
        'form_submit_text': 'Filtrar',
    }
    context.update(menu)

    return render(request, 'almoxarifado/v2/consulta_funcionario.html', context)


@login_required
@permission('almoxarifado', )
def consulta_funcionario_detalhe(request, funcionario):
    menu = menu_consultas(request)

    data_inicial = request.GET.get('data_inicial', '')
    data_final = request.GET.get('data_final', '')

    form = FormDataInicialFinal(
        initial={
            'data_inicial': data_inicial,
            'data_final': data_final,
        }
    )

    query = Q(almoxarifado_ordem_saida__user_to__username=funcionario)

    if data_inicial != '':
        data_inicial = datetime.datetime.strptime(data_inicial, "%Y-%m-%d").date()
        query = query & Q(data__gte=data_inicial)

    if data_final != '':
        data_final = datetime.datetime.strptime(data_final, "%Y-%m-%d").date()
        query = query & Q(data__lte=data_final)

    entregas = Ordem.objects.filter(query).order_by('-id')

    entregas = entregas.values(
        'id',
        'data',
        'user__first_name',
        'user__last_name',
    ).annotate(
        observacao=Min('almoxarifado_ordem_saida__observacao'),
        n_materiais=Count('almoxarifado_ordem_saida__id', distinct=True),
    )

    paginator = Paginator(entregas, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form': form,
        'form_submit_text': 'filtrar',  
        'funcionario': funcionario,
    }
    context.update(menu)

    return render(request, 'almoxarifado/v2/consulta_funcionario_detalhe.html', context)


@login_required()
@permission('almoxarifado', 'gestor', )
def consulta_funcionario_detalhe_ordem(request, funcionario, ordem):
    menu = menu_consultas(request)

    materiais = MaterialSaida.objects.filter(ordem=ordem).order_by('-quantidade')
    materiais = materiais.values(
        'ordem__id',
        'material__material',
        'quantidade',
        'data',
        'user__first_name',
        'user__last_name',
        'user_to__first_name',
        'user_to__last_name',
    )

    context = {
        'itens': materiais, 
        'ordem': ordem,
        'funcionario': funcionario,
    }
    context.update(menu)

    return render(request, 'almoxarifado/v2/consulta_funcionario_detalhe_ordem.html', context)


@login_required()
@permission('almoxarifado', )
def consulta_fornecedor(request):
    menu = menu_consultas(request)

    fornecedor = request.GET.get('q', '')

    form = FormFornecedor(
        initial={
            'q': fornecedor,
        }
    )

    query = Q(aquisicoes__id__gt=0)

    if fornecedor != '':
        query = query & Q(
            Q(nome__icontains=fornecedor) |
            Q(cnpj__icontains=fornecedor) |
            Q(aquisicoes__material__material__icontains=fornecedor)
        )

    itens = Fornecedor.objects.filter(query).annotate(
        qtde_material=Sum('aquisicoes__quantidade'),
        qtde_aq=Count('aquisicoes__material'),
        data_max=Max('aquisicoes__material__data'),
    ).order_by('nome')
    itens = itens.values(
        'nome',
        'cnpj',
        'aquisicoes__material__material',
        'aquisicoes__material__codigo',
        'data_max',
        'qtde_aq',
        'aquisicoes__material__quantidade__quantidade',
        'qtde_material',
    )

    paginator = Paginator(itens, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form': form,
        'form_submit_text': 'filtrar',
    }
    context.update(menu)

    return render(request, 'almoxarifado/v2/consulta_fornecedor.html', context)


@login_required()
@permission('almoxarifado', )
def consulta_material_saida(request):
    menu = menu_consultas(request)

    material = request.GET.get('q', '')
    data_inicial = request.GET.get('data_inicial', '')
    data_final = request.GET.get('data_final', '')

    form = FormFiltraQData(
        descricao="Nome ou ID do material",
        initial={
            'q': material,
            'data_inicial': data_inicial,
            'data_final': data_final,
        }
    )

    query = Q()

    if material != '':
        query = query & Q(
            Q(material__codigo__icontains=material) |
            Q(material__material__icontains=material)
        )

    if data_inicial != '':
        data_inicial = datetime.datetime.strptime(data_inicial, "%Y-%m-%d").date()
        query = query & Q(data__gte=data_inicial)

    if data_final != '':
        data_final = datetime.datetime.strptime(data_final, "%Y-%m-%d").date()
        query = query & Q(data__lte=data_final)

    itens = MaterialSaida.objects.filter(
        query
    ).values(
        'material__codigo',
        'material__material',
    ).annotate(
        total=Sum(F('quantidade')),
    ).order_by(
        '-total',
    )

    paginator = Paginator(itens, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form': form,
        'form_submit_text': 'filtrar',
    }
    context.update(menu)

    return render(request, 'almoxarifado/v2/consulta_material_saida.html', context)


@login_required()
@permission('almoxarifado', )
def consulta_material_saida_detalhe(request, codigo):
    menu = menu_consultas(request)

    data_inicial = request.GET.get('data_inicial', '')
    data_final = request.GET.get('data_final', '')

    form = FormDataInicialFinal(
        initial={
            'data_inicial': data_inicial,
            'data_final': data_final,
        }
    )

    query = Q(material__codigo=codigo)

    if data_inicial != '':
        data_inicial = datetime.datetime.strptime(data_inicial, "%Y-%m-%d").date()
        query = query & Q(data__gte=data_inicial)

    if data_final != '':
        data_final = datetime.datetime.strptime(data_final, "%Y-%m-%d").date()
        query = query & Q(data__lte=data_final)

    itens = MaterialSaida.objects.filter(
        query
    ).values(
        'user_to__first_name',
        'user_to__last_name',
    ).annotate(
        total=Sum(F('quantidade')),
        qtde=Count(F('id')),
    ).order_by(
        '-total',
    ).exclude(
        total__lte=0,
    )

    material = Material.objects.get(
        codigo=codigo
    )

    paginator = Paginator(itens, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form': form,
        'form_submit_text': 'filtrar',
        'material_codigo': material.codigo,
        'material_material': material.material,
    }
    context.update(menu)

    return render(request, 'almoxarifado/v2/consulta_material_saida_detalhe.html', context)


@login_required()
@permission('almoxarifado', )
def consulta_fornecedor_detalhe(request, material):
    menu = menu_consultas(request)

    itens = MaterialEntrada.objects.filter(material__codigo=material).values(
        'fornecedor__nome',
        'material__quantidade__quantidade',
        'ordem__id',
        'quantidade',
        'user__first_name',
        'user__last_name',
        'data',
    ).order_by('-data')

    material = Material.objects.get(codigo=material)

    paginator = Paginator(itens, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'material': material,
    }
    context.update(menu)

    return render(request, 'almoxarifado/v2/consulta_fornecedor_detalhe.html', context)


@login_required()
@permission('almoxarifado', )
def view_cadastrar_usuario_passivo(request, callback=None):
    """
        View de cadastro de novos usuários passivos.
        :param callback: próxima página
        :param request: POST form
        :return:
        """

    if request.method == 'POST':
        form = FormCadastraUsuarioPassivo(request.POST)

        if form.is_valid():
            form.save()
            user = User.objects.get(username=form.cleaned_data['username'])
            user_type = UserType(user=user)
            user_type.save()

            if callback is not None:

                if callback == 'lista':

                    return HttpResponseRedirect('/almoxarifado/menu-saidas/lista/')

            return HttpResponseRedirect('/almoxarifado/menu-cadastros/')
    else:
        form = FormCadastraUsuarioPassivo()

    if callback is not None:
        context = {
            'form': form,
            'callback': 'almoxarifado_saida_lista',
            'button_submit_text': 'Cadastrar beneficiário',
            'callback_text': 'Cancelar',
            'pagina_titulo': 'Almoxarifado',
            'menu_titulo': 'Cadastro de técnico',
        }

    else:
        context = {
            'form': form,
            'callback': 'almoxarifado_menu_cadastros',
            'button_submit_text': 'Cadastrar beneficiário',
            'callback_text': 'Cancelar',
            'pagina_titulo': 'Almoxarifado',
            'menu_titulo': 'Cadastro de técnico',
        }

    return render(request, 'almoxarifado/cadastra_usuario_passivo.html', context)
