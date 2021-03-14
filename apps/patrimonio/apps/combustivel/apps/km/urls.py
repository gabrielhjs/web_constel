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
        views.view_registrar_km_inicial,
        name='patrimonio_combustivel_km_registros'
    ),
    path(
        'patrimonio/combustivel/km/registros/inicial/<int:user_id>/',
        views.view_registrar_km_inicial_detalhes,
        name='patrimonio_combustivel_km_registros_inicial',
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
]
