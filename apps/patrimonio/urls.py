from django.urls import path

from . import views


urlpatterns = [
    path(
        'patrimonio/',
        views.view_menu_principal,
        name='patrimonio_menu_principal',
    ),
    path(
        'patrimonio/menu-cadastros/',
        views.view_menu_cadastros,
        name='patrimonio_menu_cadastros',
    ),
    path(
        'patrimonio/menu-cadastros/ferramenta/',
        views.view_cadastrar_ferramenta,
        name='patrimonio_cadastrar_ferramenta',
    ),
    path(
        'patrimonio/menu-cadastros/patrimonio/',
        views.view_cadastrar_patrimonio,
        name='patrimonio_cadastrar_patrimonio',
    ),
    path(
        'patrimonio/menu-entradas/',
        views.view_menu_entradas,
        name='patrimonio_menu_entradas',
    ),
    path(
        'patrimonio/menu-entradas/ferramentas/',
        views.view_entrada_ferramenta,
        name='patrimonio_entrada_ferramenta',
    ),
    path(
        'patrimonio/menu-entradas/patrimonio/',
        views.view_entrada_patrimonio,
        name='patrimonio_entrada_patrimonio',
    ),
    path(
        'patrimonio/menu-consultas/',
        views.view_menu_consultas,
        name='patrimonio_menu_consultas',
    ),
    path(
        'patrimonio/menu-consultas/ferramenta/',
        views.view_consulta_ferramentas,
        name='patrimonio_consulta_ferramentas',
    ),
    path(
        'patrimonio/menu-consultas/ferramenta/estoque/',
        views.view_consulta_ferramentas_estoque,
        name='patrimonio_consulta_ferramentas_estoque',
    ),
    path(
        'patrimonio/menu-consultas/patrimonio/',
        views.view_consulta_patrimonio,
        name='patrimonio_consulta_patrimonios',
    ),
    path(
        'patrimonio/menu-relatorios/',
        views.view_menu_relatorios,
        name='patrimonio_menu_relatorios',
    ),
]
