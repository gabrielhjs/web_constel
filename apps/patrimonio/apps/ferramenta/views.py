from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from .forms import *
from .models import *

from constel.apps.controle_acessos.decorator import permission
from ...menu import menu_principal, menu_cadastros, menu_entradas, menu_saidas, menu_consultas, menu_consultas_modelos

from constel.forms import FormFiltraQ


@login_required
@permission('patrimonio', )
def cadastra_ferramenta(request):
    menu = menu_cadastros(request)

    if request.method == 'POST':
        form = FormCadastraFerramenta(request.POST)

        if form.is_valid():
            ferramenta = Ferramenta(
                nome=form.cleaned_data['nome'],
                descricao=form.cleaned_data['descricao'],
                user=request.user,
            )
            ferramenta.save()
            FerramentaQuantidade(
                ferramenta=ferramenta,
                quantidade=0,
            ).save()

            return HttpResponseRedirect('/patrimonio/cadastros/ferramenta')
    else:
        form = FormCadastraFerramenta()

    itens = Ferramenta.objects.values(
        'nome',
        'data',
        'user__first_name',
        'user__last_name',
    ).order_by('-data')

    paginator = Paginator(itens, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form': form,
        'form_submit_text': 'Cadastrar nova ferramenta',
    }
    context.update(menu)

    return render(request, 'ferramenta/v2/cadastra_ferramenta.html', context)


@login_required
@permission('patrimonio', )
def entrada_ferramenta(request):
    menu = menu_entradas(request)

    if request.method == 'POST':
        form = FormEntradaFerramenta(request.POST)

        if form.is_valid():
            FerramentaEntrada(
                ferramenta=form.cleaned_data['ferramenta'],
                quantidade=form.cleaned_data['quantidade'],
                valor=form.cleaned_data['valor'],
                observacao=form.cleaned_data['observacao'],
                user=request.user,
            ).save()
            ferramenta = form.cleaned_data['ferramenta']
            ferramenta.quantidade.quantidade += form.cleaned_data['quantidade']
            ferramenta.quantidade.save()

            return HttpResponseRedirect('/patrimonio/entradas/ferramenta')

    else:
        form = FormEntradaFerramenta()

    context = {
        'form': form,
        'form_submit_text': 'Registrar entrada',
    }
    context.update(menu)

    return render(request, 'patrimonio/v2/entrada.html', context)


@login_required
@permission('patrimonio', )
def saida_ferramenta(request):
    menu = menu_saidas(request)

    if request.method == 'POST':
        form = FormSaidaFerramenta(request.POST)

        if form.is_valid():
            saida = FerramentaSaida(
                ferramenta=form.cleaned_data['ferramenta'],
                quantidade=form.cleaned_data['quantidade'],
                observacao=form.cleaned_data['observacao'],
                user_to=form.cleaned_data['user_to'],
                user=request.user,
            )
            ferramenta = form.cleaned_data['ferramenta']
            ferramenta.quantidade.quantidade -= form.cleaned_data['quantidade']

            if FerramentaQuantidadeFuncionario.objects.filter(
                user=form.cleaned_data['user_to'],
                ferramenta=ferramenta
            ).exists():

                carga = FerramentaQuantidadeFuncionario.objects.get(
                    user=form.cleaned_data['user_to'],
                    ferramenta=ferramenta
                )
                carga.quantidade += form.cleaned_data['quantidade']

            else:
                carga = FerramentaQuantidadeFuncionario(
                    user=form.cleaned_data['user_to'],
                    ferramenta=ferramenta,
                    quantidade=form.cleaned_data['quantidade']
                )

            ferramenta.quantidade.save()
            saida.save()
            carga.save()

            return HttpResponseRedirect('/patrimonio/saidas/ferramenta')

    else:
        form = FormSaidaFerramenta()

    context = {
        'form': form,
        'form_submit_text': 'Registrar entrega',
    }
    context.update(menu)

    return render(request, 'patrimonio/v2/entrada.html', context)


@login_required
@permission('patrimonio', )
def fechamento_ferramenta(request):
    menu = menu_principal(request)

    if request.method == 'POST':
        form = FormFechamentoFerramenta(request.POST)

        if form.is_valid():
            ferramenta = form.cleaned_data['ferramenta']
            status = form.cleaned_data['status']

            fechamento = FerramentaFechamento(
                ferramenta=ferramenta,
                status=form.cleaned_data['status'],
                quantidade=form.cleaned_data['quantidade'],
                observacao=form.cleaned_data['observacao'],
                user_from=form.cleaned_data['user_from'],
                user=request.user,
            )

            print(status)

            if int(status) == 0:
                ferramenta.quantidade.quantidade += form.cleaned_data['quantidade']
                messages.success(request, 'Fechamento realizado e ferramentas (RE)inseridas no estoque')

            else:
                messages.success(request, 'Fechamento realizado')

            carga = FerramentaQuantidadeFuncionario.objects.get(
                user=form.cleaned_data['user_from'],
                ferramenta=ferramenta
            )
            carga.quantidade -= form.cleaned_data['quantidade']

            fechamento.save()
            ferramenta.quantidade.save()
            carga.save()

            return HttpResponseRedirect('/patrimonio/fechamento/ferramenta')

    else:
        form = FormFechamentoFerramenta()

    context = {
        'form': form,
        'form_submit_text': 'Registrar fechamento',
    }
    context.update(menu)

    return render(request, 'patrimonio/v2/entrada.html', context)


@login_required
@permission('patrimonio', )
def consulta_ferramenta(request):
    menu = menu_consultas_modelos(request)

    ferramenta = request.GET.get('q', '')

    form = FormFiltraQ(
        descricao="ferramenta",
        initial={
            'q': ferramenta,
        }
    )

    query = Q()

    if ferramenta != '':
        query = query & Q(nome__icontains=ferramenta)

    itens = Ferramenta.objects.filter(
        query
    ).values(
        'id',
        'nome',
        'descricao',
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

    return render(request, 'ferramenta/v2/consulta_ferramenta.html', context=context)


def edita_modelo_ferramenta(request, modelo_id):
    menu = menu_consultas_modelos(request)

    modelo = Ferramenta.objects.get(id=modelo_id)

    form = FormEditaModeloFerramenta(data=request.POST or None, instance=modelo)

    if request.method == 'POST':

        if form.is_valid():
            form.save()

            messages.success(request, 'Alterações salvas com sucesso')

            return HttpResponseRedirect(f'/patrimonio/edicao/ferramenta/modelo/{modelo_id}')

    context = {
        'form': form,
        'form_submit_text': 'Salvar alterações',
    }
    context.update(menu)

    return render(request, 'ferramenta/v2/edita_modelo_ferramenta.html', context)


@login_required
@permission('patrimonio', )
def consulta_ferramenta_estoque(request):
    menu = menu_consultas(request)

    ferramenta = request.GET.get('q', '')

    form = FormFiltraQ(
        descricao="ferramenta",
        initial={
            'q': ferramenta,
        }
    )

    query = Q()

    if ferramenta != '':
        query = query & Q(ferramenta__nome__icontains=ferramenta)

    itens = FerramentaQuantidade.objects.filter(
        query
    ).values(
        'ferramenta__nome',
        'quantidade',
    ).exclude(
        quantidade__lte=0,
    ).order_by('ferramenta__nome')

    paginator = Paginator(itens, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'form': form,
        'form_submit_text': 'Filtrar',
        'page_obj': page_obj,
    }
    context.update(menu)

    return render(request, 'ferramenta/v2/consulta_ferramenta_estoque.html', context=context)
