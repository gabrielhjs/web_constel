from django.urls import path, include

from . import views


urlpatterns = [
    path('', include('apps.almoxarifado.apps.lista_saida.urls')),

    path(
        'almoxarifado/',
        views.view_menu_principal,
        name='almoxarifado_menu_principal',
    ),
    path(
        'almoxarifado/menu-cadastros/',
        views.view_menu_cadastros,
        name='almoxarifado_menu_cadastros',
    ),
    path(
        'almoxarifado/menu-cadastros/material/',
        views.view_cadastrar_material,
        name='almoxarifado_cadastrar_material',
    ),
    path(
        'almoxarifado/menu-cadastros/fornecedor/',
        views.view_cadastrar_fornecedor,
        name='almoxarifado_cadastrar_fornecedor',
    ),
    path(
        'almoxarifado/menu-entradas/',
        views.view_menu_entradas,
        name='almoxarifado_menu_entradas',
    ),
    path(
        'almoxarifado/menu-entradas/material/',
        views.view_entrada_material,
        name='almoxarifado_entrada_material',
    ),
    path(
        'almoxarifado/menu-saidas/',
        views.view_menu_saidas,
        name='almoxarifado_menu_saidas',
    ),
    path(
        'almoxarifado/menu-saidas/material/',
        views.view_saida_material_individual,
        name='almoxarifado_saida_material_individual',
    ),
    path(
        'almoxarifado/menu-saidas/materiais/1/',
        views.view_saida_materiais1,
        name='almoxarifado_saida_materiais1',
    ),
    path(
        'almoxarifado/menu-saidas/materiais/2/',
        views.view_saida_materiais2,
        name='almoxarifado_saida_materiais2',
    ),
    path(
        'almoxarifado/menu-consultas/',
        views.view_menu_consultas,
        name='almoxarifado_menu_consultas',
    ),
    path(
        'almoxarifado/menu-consultas/materiais/',
        views.ViewConsultaMateriais.as_view(),
        name='almoxarifado_consulta_materiais',
    ),
    path(
        'almoxarifado/menu-consultas/estoque/',
        views.view_consulta_estoque,
        name='almoxarifado_consulta_estoque',
    ),
    path(
        'almoxarifado/menu-consultas/ordens/<int:tipo>/',
        views.view_consulta_ordem,
        name='almoxarifado_consulta_ordens',
    ),
    path(
        'almoxarifado/menu-relatorios/',
        views.view_menu_relatorios,
        name='almoxarifado_menu_relatorios',
    ),
]
