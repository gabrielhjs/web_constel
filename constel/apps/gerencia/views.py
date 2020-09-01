from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models.functions import TruncMonth, TruncWeek, Coalesce
from django.db.models import Sum, Count, Avg, F, Q

from ..controle_acessos.decorator import permission

from apps.patrimonio.apps.combustivel.apps.talao.models import EntregaVale
from apps.almoxarifado.models import MaterialSaida
from apps.almoxarifado.apps.cont.models import OntSaida, OntEntrada

from .menu import menu_principal


@login_required
@permission('gerencia')
def index(request):
    menu = menu_principal(request)

    combustivel = EntregaVale.objects.all().annotate(
        mes=TruncMonth('data')
    ).values(
        'mes'
    ).annotate(
        total=Sum('valor'),
        avg=Avg('valor'),
        qtd=Count('valor'),
    ).order_by(
        'mes'
    )

    almoxarifado = MaterialSaida.objects.all().annotate(
        mes=TruncMonth('data',)
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

    ont_entrada = OntEntrada.objects.annotate(
        mes=TruncMonth('data')
    ).values(
        'mes',
    ).annotate(
        total=Count('id')
    ).order_by(
        'mes'
    )

    ont_saida = OntSaida.objects.all().annotate(
        mes=TruncMonth('data')
    ).values(
        'mes',
    ).annotate(
        total=Count('id')
    ).order_by(
        'mes'
    )

    context = {
        'combustivel': combustivel,
        'almoxarifado': almoxarifado,
        'ont_entrada': ont_entrada,
        'ont_saida': ont_saida,
    }
    context.update(menu)

    return render(request, 'gerencia/dashboard.html', context)
