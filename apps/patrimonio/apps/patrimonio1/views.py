from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Subquery, OuterRef, Max

from .forms import *
from .models import *
from constel.apps.controle_acessos.decorator import permission

from ...menu import menu_cadastros, menu_entradas, menu_saidas, menu_consultas, menu_consultas_modelos

from constel.forms import FormFiltraQ


@login_required
@permission('patrimonio', )
def cadastra_patrimonio(request):
    menu = menu_cadastros(request)

    if request.method == 'POST':
        form = FormCadastraPatrimonio(request.POST)

        if form.is_valid():
            Patrimonio(
                nome=form.cleaned_data['nome'],
                descricao=form.cleaned_data['descricao'],
                user=request.user,
            ).save()

            return HttpResponseRedirect('/patrimonio/cadastros/patrimonio')
    else:
        form = FormCadastraPatrimonio()

    itens = Patrimonio.objects.values(
        'nome',
        'data',
        'user__first_name',
        'user__last_name',
    ).order_by(
        '-data'
    )

    paginator = Paginator(itens, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form': form,
        'form_submit_text': 'Cadastrar modelo de patrimônio',
    }
    context.update(menu)

    return render(request, 'patrimonio1/v2/cadastra_patrimonio.html', context)


@login_required
@permission('patrimonio', )
def entrada_patrimonio_1(request):
    menu = menu_entradas(request)

    if request.method == 'POST':
        initial = {
            'codigo': request.session.get('patrimonio_entrada_codigo', None),
        }
        form = FormEntradaPatrimonio1(data=request.POST, initial=initial)

        if form.is_valid():
            request.session['patrimonio_entrada_codigo'] = form.cleaned_data['codigo']

            return HttpResponseRedirect('/patrimonio/entradas/patrimonio_2')

    else:
        form = FormEntradaPatrimonio1()

    context = {
        'form': form,
        'form_submit_text': 'Avançar',
    }
    context.update(menu)

    return render(request, 'patrimonio/v2/entrada.html', context)


def entrada_patrimonio_2(request):
    menu = menu_entradas(request)

    if request.session.get('patrimonio_entrada_codigo') is None:
        return HttpResponseRedirect('/patrimonio/entradas/patrimonio_1')

    codigo = request.session.get('patrimonio_entrada_codigo')

    if PatrimonioId.objects.filter(codigo=codigo).exists():
        patrimonio = PatrimonioId.objects.get(codigo=codigo)

        if patrimonio.status != 0:
            PatrimonioEntrada1(
                patrimonio=patrimonio,
                user=request.user
            ).save()

            patrimonio.status = 0
            patrimonio.save()

            messages.success(request, 'Patrimônio (RE)inserido no estoque com sucesso')

        else:
            messages.error(request, 'Patrimônio já em estoque')

        return HttpResponseRedirect('/patrimonio/entradas/patrimonio_1')

    else:

        if request.method == 'POST':
            form = FormEntradaPatrimonio2(request.POST)

            if form.is_valid():
                patrimonio = PatrimonioId(
                    codigo=request.session.get('patrimonio_entrada_codigo'),
                    status=0,
                    patrimonio=form.cleaned_data['patrimonio'],
                    valor=form.cleaned_data['valor'],
                )
                patrimonio.save()

                PatrimonioEntrada1(
                    patrimonio=patrimonio,
                    user=request.user
                ).save()

                messages.success(request, 'Patrimônio cadastrado e inserido no estoque com sucesso')

                return HttpResponseRedirect('/patrimonio/entradas/patrimonio_1')

        else:
            form = FormEntradaPatrimonio2()

        context = {
            'form': form,
            'form_submit_text': 'Inserir em estoque',
        }
        context.update(menu)

        return render(request, 'patrimonio/v2/entrada.html', context)


@login_required
@permission('patrimonio', )
def saida_patrimonio(request):
    menu = menu_saidas(request)

    if request.method == 'POST':
        form = FormSaidaPatrimonio(request.POST)

        if form.is_valid():
            patrimonio = form.cleaned_data['patrimonio']

            entrada = PatrimonioEntrada1.objects.filter(
                patrimonio=patrimonio,
            ).last()

            print(entrada)

            PatrimonioSaida(
                entrada=entrada,
                patrimonio=patrimonio,
                observacao=form.cleaned_data['observacao'],
                user=request.user,
                user_to=form.cleaned_data['user_to'],
            ).save()
            patrimonio.status = 1
            patrimonio.save()

            messages.success(request, 'Entrega registrada com sucesso')

            return HttpResponseRedirect('/patrimonio/saidas/patrimonio')

    else:
        form = FormSaidaPatrimonio()

    context = {
        'form': form,
        'form_submit_text': 'Registrar entrega',
    }
    context.update(menu)

    return render(request, 'patrimonio/v2/entrada.html', context)


@login_required
@permission('patrimonio', )
def consulta_patrimonio(request):
    menu = menu_consultas_modelos(request)

    patrimonio = request.GET.get('q', '')

    form = FormFiltraQ(
        descricao="patrimônio",
        initial={
            'q': patrimonio,
        }
    )

    query = Q()

    if patrimonio != '':
        query = query & Q(nome__icontains=patrimonio)

    itens = Patrimonio.objects.filter(
        query
    ).values(
        'nome',
        'data',
        'user__first_name',
        'user__last_name',
    ).order_by('nome')

    paginator = Paginator(itens, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'form': form,
        'form_submit_text': 'Filtrar',
        'page_obj': page_obj,
    }
    context.update(menu)

    return render(request, 'patrimonio1/v2/consulta_patrimonio.html', context=context)


@login_required
@permission('patrimonio', )
def consulta_patrimonio_status(request):
    menu = menu_consultas(request)

    patrimonio = request.GET.get('q', '')

    form = FormFiltraQ(
        descricao="patrimônio",
        initial={
            'q': patrimonio,
        }
    )

    query = Q()

    if patrimonio != '':
        query = query & Q(
            Q(codigo__icontains=patrimonio) |
            Q(patrimonio__nome__icontains=patrimonio)
        )

    subquery = PatrimonioSaida.objects.filter(
        patrimonio=OuterRef('pk')
    ).values(
        'user_to__first_name',
        'user_to__last_name',
    ).annotate(
        ultima_data=Max('data')
    )

    itens = PatrimonioId.objects.filter(
        query
    ).annotate(
        user_to_first_name=Subquery(subquery.values('user_to__first_name')),
        user_to_last_name=Subquery(subquery.values('user_to__last_name')),
        ultima_entrega=Subquery(subquery.values('ultima_data')),
    ).values(
        'codigo',
        'patrimonio__nome',
        'status',
        'user_to_first_name',
        'user_to_last_name',
        'ultima_entrega',
    ).order_by('patrimonio__nome', 'codigo')

    paginator = Paginator(itens, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'form': form,
        'form_submit_text': 'Filtrar',
        'page_obj': page_obj,
    }
    context.update(menu)

    return render(request, 'patrimonio1/v2/consulta_patrimonio_status.html', context=context)
