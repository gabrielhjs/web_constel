from django.urls import path

from . import views


urlpatterns = [
    path(
        'patrimonio/combustivel/km/',
        views.view_menu_principal,
        name='patrimonio_combustivel_km'
    ),
    path(
        'patrimonio/combustivel/km/registros/',
        views.view_menu_registros,
        name='patrimonio_combustivel_km_registros'
    ),
    path(
        'patrimonio/combustivel/km/registros/inicial/',
        views.view_registrar_km_inicial,
        name='patrimonio_combustivel_km_registros_inicial'
    ),
    path(
        'patrimonio/combustivel/km/registros/final/',
        views.view_registrar_km_final,
        name='patrimonio_combustivel_km_registros_final'
    ),
    path(
        'patrimonio/combustivel/km/registros/inicial/<int:user_id>/',
        views.view_registrar_km_inicial_detalhes,
        name='patrimonio_combustivel_km_registros_inicial_detalhes',
    ),
    path(
        'patrimonio/combustivel/km/registros/final/<int:user_id>/<int:km_id>/',
        views.view_registrar_km_final_detalhes,
        name='patrimonio_combustivel_km_registros_final_detalhes',
    ),
    path(
        'patrimonio/combustivel/km/consultas/',
        views.view_menu_consultas,
        name='patrimonio_combustivel_km_consultas'
    ),
    path(
        'patrimonio/combustivel/km/consultas/equipe/',
        views.view_consulta_km_time,
        name='patrimonio_combustivel_km_consultas_time'
    ),
    path(
        'patrimonio/combustivel/km/consultas/hoje/',
        views.view_consulta_km_hoje,
        name='patrimonio_combustivel_km_consultas_hoje'
    ),
    path(
        'patrimonio/combustivel/km/consultas/pendencias/hoje/',
        views.view_consulta_km_pendencias_hoje,
        name='patrimonio_combustivel_km_consultas_pendencias_hoje'
    ),
    path(
        'patrimonio/combustivel/km/relatorios/',
        views.view_menu_relatorios,
        name='patrimonio_combustivel_km_relatorios'
    ),
    path(
        'patrimonio/combustivel/km/relatorios/geral/',
        views.view_relatorio_geral,
        name='patrimonio_combustivel_km_relatorios_geral'
    ),
]
