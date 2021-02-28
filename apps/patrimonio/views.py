import datetime

from django.core.paginator import Paginator
from django.db.models import Q, Min, Case, When, F
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from constel.apps.controle_acessos.decorator import permission
from constel.forms import FormDataInicialFinal
from .apps.ferramenta.models import FerramentaSaida
from .apps.patrimonio1.models import PatrimonioSaida

from .menu import (
    menu_principal,
    menu_cadastros,
    menu_entradas,
    menu_saidas,
    menu_consultas,
    menu_consultas_modelos,
)
from .models import Ordem


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
def consultas_ordem_saida(request: HttpRequest) -> HttpResponse:
    menu = menu_consultas(request)

    data_inicial = request.GET.get('data_inicial', '')
    data_final = request.GET.get('data_final', '')

    form = FormDataInicialFinal(
        initial={
            'data_inicial': data_inicial,
            'data_final': data_final,
        }
    )

    query = Q(Q(tipo=1) & Q(Q(saida_ordem_ferramenta__id__gte=0) | Q(saida_ordem_patrimonio__id__gte=0)))

    if data_inicial != '':
        data_inicial = datetime.datetime.strptime(data_inicial, "%Y-%m-%d").date()
        query = query & Q(data__gte=data_inicial)

    if data_final != '':
        data_final = datetime.datetime.strptime(data_final, "%Y-%m-%d").date()
        query = query & Q(data__lte=data_final)

    itens = Ordem.objects.filter(query).order_by(
        '-data'
    ).annotate(
        user_to_first_name1=Min('saida_ordem_ferramenta__user_to__first_name'),
        user_to_last_name1=Min('saida_ordem_ferramenta__user_to__last_name'),
        user_to_first_name2=Min('saida_ordem_patrimonio__user_to__first_name'),
        user_to_last_name2=Min('saida_ordem_patrimonio__user_to__last_name'),
    ).values(
        'id',
        'data',
        'user__first_name',
        'user__last_name',
        'user_to_first_name1',
        'user_to_last_name1',
        'user_to_first_name2',
        'user_to_last_name2',
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

    return render(request, 'patrimonio/v2/consulta_ordem.html', context)


@login_required()
@permission('patrimonio', )
def consultas_ordem_saida_detalhe(request, **kwargs):
    menu = menu_consultas(request)

    if Ordem.objects.filter(id=kwargs.get('ordem')).exists():
        menu = menu_consultas(request)
        ordem = Ordem.objects.get(id=kwargs.get('ordem'))

        ferramentas = FerramentaSaida.objects.filter(ordem=ordem).values(
            "ferramenta__nome",
            "quantidade",
        )

        patrimonios = PatrimonioSaida.objects.filter(ordem=ordem).values(
            "patrimonio__codigo",
            "patrimonio__patrimonio__nome"
        )

        context = {
            'ferramentas': ferramentas,
            'patrimonios': patrimonios,
            'ordem': ordem,
        }
        context.update(menu)

        return render(request, 'patrimonio/v2/consulta_ordem_detalhe.html', context)

    else:
        return HttpResponseRedirect('/patrimonio/consultas/')


@login_required
@permission('patrimonio', )
def consultas_modelos(request):
    context = menu_consultas_modelos(request)

    return render(request, 'constel/v2/app.html', context)
