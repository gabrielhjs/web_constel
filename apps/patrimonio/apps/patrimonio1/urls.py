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
        'patrimonio/menu-saidas/patrimonio/',
        views.view_saida_patrimonio,
        name='patrimonio_saida_patrimonio',
    ),
    path(
        'patrimonio/menu-consultas/patrimonio-modelo/',
        views.view_consulta_patrimonios_modelos,
        name='patrimonio_consulta_patrimonios_modelos',
    ),
    path(
        'patrimonio/menu-consultas/patrimonio/',
        views.view_consulta_patrimonios,
        name='patrimonio_consulta_patrimonios',
    ),

    # Novas urls

    path(
        'patrimonio/cadastros/patrimonio/',
        views.cadastra_patrimonio,
        name='patrimonio_cadastrar_patrimonio',
    ),
    path(
        'patrimonio/entradas/patrimonio/',
        views.entrada_patrimonio,
        name='patrimonio_entrada_patrimonio',
    ),
    path(
        'patrimonio/saidas/patrimonio/',
        views.saida_patrimonio,
        name='patrimonio_saida_patrimonio',
    ),
]
