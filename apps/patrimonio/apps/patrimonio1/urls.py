from django.urls import path

from . import views


urlpatterns = [
    path(
        'patrimonio/menu-cadastros/patrimonio/',
        views.view_cadastrar_patrimonio,
        name='patrimonio_cadastrar_patrimonio',
    ),
    path(
        'patrimonio/menu-entradas/patrimonio/',
        views.view_entrada_patrimonio,
        name='patrimonio_entrada_patrimonio',
    ),
    path(
        'patrimonio/menu-consultas/patrimonio/',
        views.view_consulta_patrimonio,
        name='patrimonio_consulta_patrimonios',
    ),
]
