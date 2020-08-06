from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .forms import *
from .models import *

from constel.apps.controle_acessos.decorator import permission
from ...menu import menu_cadastros, menu_entradas, menu_saidas


@login_required
@permission('patrimonio', )
def view_cadastrar_ferramenta(request):

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

            return HttpResponseRedirect('/patrimonio/menu-cadastros/')
    else:
        form = FormCadastraFerramenta()

    context = {
        'ferramentas': Ferramenta.objects.all().order_by('nome'),
        'form': form,
        'pagina_titulo': 'Patrimônio',
        'menu_titulo': 'Cadastro de ferramenta',
        'callback': 'patrimonio_menu_cadastros',
        'button_submit_text': 'Cadastrar ferramenta',
        'callback_text': 'Cancelar',
    }

    return render(request, 'ferramenta/cadastrar_ferramenta.html', context)


@login_required
@permission('patrimonio', )
def view_entrada_ferramenta(request):

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

            return HttpResponseRedirect('/patrimonio/menu-entradas/')

    else:
        form = FormEntradaFerramenta()

    context = {
        'form': form,
        'callback': 'patrimonio_menu_entradas',
        'button_submit_text': 'Registrar entrada',
        'callback_text': 'Cancelar',
        'pagina_titulo': 'Patrimônio',
        'menu_titulo': 'Aquisição de ferramenta',
    }

    return render(request, 'patrimonio/entrada.html', context)


@login_required
@permission('patrimonio', )
def view_saida_ferramenta(request):

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

            ferramenta.quantidade.save()
            saida.save()

            return HttpResponseRedirect('/patrimonio/menu-saidas/')

    else:
        form = FormSaidaFerramenta()

    context = {
        'form': form,
        'callback': 'patrimonio_menu_saidas',
        'button_submit_text': 'Registrar entrega',
        'callback_text': 'Cancelar',
        'pagina_titulo': 'Patrimônio',
        'menu_titulo': 'Entrega de ferramenta',
    }

    return render(request, 'patrimonio/entrada.html', context)


@login_required
@permission('patrimonio', )
def view_consulta_ferramentas(request):

    context = {
        'ferramentas': Ferramenta.objects.all().order_by('nome'),
        'pagina_titulo': 'Patrimônio',
        'menu_titulo': 'Ferramentas cadastradas',
    }

    return render(request, 'ferramenta/consulta_ferramenta.html', context=context)


@login_required
@permission('patrimonio', )
def view_consulta_ferramentas_estoque(request):

    context = {
        'ferramentas': FerramentaQuantidade.objects.all().order_by('ferramenta__nome'),
        'pagina_titulo': 'Patrimônio',
        'menu_titulo': 'Estoque de ferramentas',
    }

    return render(request, 'ferramenta/consulta_ferramenta_estoque.html', context=context)


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

            ferramenta.quantidade.save()
            saida.save()

            return HttpResponseRedirect('/patrimonio/saidas/ferramenta')

    else:
        form = FormSaidaFerramenta()

    context = {
        'form': form,
        'form_submit_text': 'Registrar entrega',
    }
    context.update(menu)

    return render(request, 'patrimonio/v2/entrada.html', context)
