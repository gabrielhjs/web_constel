from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, ExpressionWrapper, Value, F, CharField
from django.http import FileResponse

from .forms import *
from .models import *
from constel.apps.controle_acessos.decorator import permission

from ...menu import menu_cadastros, menu_entradas, menu_saidas, menu_consultas, menu_consultas_modelos
from ..pdf.objects import FichaPatrimonio

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

            patrimonio_saida = PatrimonioSaida(
                entrada=entrada,
                patrimonio=patrimonio,
                observacao=form.cleaned_data['observacao'],
                user=request.user,
                user_to=form.cleaned_data['user_to'],
            )
            patrimonio_saida.save()
            patrimonio.status = 1
            patrimonio.save()

            messages.success(request, 'Entrega registrada com sucesso')

            return HttpResponseRedirect(f'/patrimonio/saidas/patrimonio/conclui/{patrimonio_saida.id}/')

    else:
        form = FormSaidaPatrimonio()

    context = {
        'form': form,
        'form_submit_text': 'Registrar entrega',
    }
    context.update(menu)

    return render(request, 'patrimonio/v2/entrada.html', context)


@login_required
@permission('almoxarifado', 'almoxarifado - saida', )
def saida_patrimonio_conclui(request, ordem_id):
    menu = menu_saidas(request)

    context = {
        'ordem_id': ordem_id,
    }
    context.update(menu)

    return render(request, 'patrimonio1/v2/conclui.html', context)


@login_required
@permission('almoxarifado', 'almoxarifado - saida', )
def saida_patrimonio_imprime(request, ordem_id):

    if PatrimonioSaida.objects.filter(id=ordem_id).exists():
        data = PatrimonioSaida.objects.get(id=ordem_id)

    else:
        return HttpResponseRedirect('/patrimonio/saidas/patrimonio/')

    ficha = FichaPatrimonio(data)

    return FileResponse(ficha.file(), filename='ficha_patrimonio' + str(data.id) + '.pdf')


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

    return render(request, 'patrimonio1/v2/consulta_patrimonio.html', context=context)


def edita_modelo_patrimonio(request, modelo_id):
    menu = menu_consultas_modelos(request)

    modelo_patrimonio = Patrimonio.objects.get(id=modelo_id)

    form = FormEditaModeloPatrimonio(data=request.POST or None, instance=modelo_patrimonio)

    if request.method == 'POST':

        if form.is_valid():
            form.save()

            messages.success(request, 'Alterações salvas com sucesso')

            return HttpResponseRedirect(f'/patrimonio/edicao/patrimonio/modelo/{modelo_id}')

    context = {
        'form': form,
        'form_submit_text': 'Salvar alterações',
    }
    context.update(menu)

    return render(request, 'patrimonio1/v2/edita_modelo_patrimonio.html', context)


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

    itens = PatrimonioId.objects.filter(query).order_by('patrimonio__nome', 'codigo')

    print(itens.values_list())

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


def edita_patrimonio(request, patrimonio_id):
    menu = menu_consultas_modelos(request)

    patrimonio = PatrimonioId.objects.get(id=patrimonio_id)

    form = FormEditaPatrimonio(data=request.POST or None, instance=patrimonio)

    if request.method == 'POST':

        if form.is_valid():
            form.save()

            messages.success(request, 'Alterações salvas com sucesso')

            return HttpResponseRedirect(f'/patrimonio/edicao/patrimonio/{patrimonio_id}')

    context = {
        'form': form,
        'form_submit_text': 'Salvar alterações',
    }
    context.update(menu)

    return render(request, 'patrimonio1/v2/edita_patrimonio.html', context)


def consulta_patrimonio_status_detalhe(request, patrimonio):
    menu = menu_consultas(request)

    patrimonio = PatrimonioId.objects.get(codigo=patrimonio)

    entradas = patrimonio.patrimonio_entrada.values(
        'patrimonio__codigo',
        'data',
        'user__first_name',
        'user__last_name',
    ).annotate(
        tipo=Value("Entrada", output_field=CharField()),
        user_to_first_name=Value(None, output_field=CharField()),
        user_to_last_name=Value(None, output_field=CharField()),
    )

    saidas = patrimonio.patrimonio_saida.values(
        'patrimonio__codigo',
        'data',
        'user__first_name',
        'user__last_name',
    ).annotate(
        tipo=Value("Saída", output_field=CharField()),
        user_to_first_name=ExpressionWrapper(F('user_to__first_name'), output_field=CharField()),
        user_to_last_name=ExpressionWrapper(F('user_to__last_name'), output_field=CharField()),
    )

    paginator = Paginator(
        entradas.union(
            saidas,
            all=True
        ).values(
            'patrimonio__codigo',
            'data',
            'user__first_name',
            'user__last_name',
            'user_to_first_name',
            'user_to_last_name',
            'tipo',
        ).order_by('-data'),
        50
    )

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'patrimonio': patrimonio,
    }
    context.update(menu)

    return render(request, "patrimonio1/v2/consulta_patrimonio_status_detalhe.html", context)
