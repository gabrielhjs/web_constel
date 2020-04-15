from django.urls import path, include

from . import views


urlpatterns = [
    path('', include('apps.almoxarifado.apps.cont.api.urls')),

    path(
        'almoxarifado/cont/',
        views.view_menu_principal,
        name='almoxarifado_cont_menu_principal',
    ),
    path(
        'almoxarifado/cont/menu-cadastros/',
        views.view_menu_cadastros,
        name='almoxarifado_cont_menu_cadastros',
    ),
    path(
        'almoxarifado/cont/menu-consultas/',
        views.view_menu_consultas,
        name='almoxarifado_cont_menu_consultas',
    ),
    path(
        'almoxarifado/cont/menu-cadastros/secao/',
        views.view_cadastrar_secao,
        name='almoxarifado_cont_cadastrar_secao',
    ),
    path(
        'almoxarifado/cont/menu-cadastros/modelo/',
        views.view_cadastrar_modelo,
        name='almoxarifado_cont_cadastrar_modelo',
    ),
    path(
        'almoxarifado/cont/menu-consultas/situacao/',
        views.view_consulta_situacao,
        name='almoxarifado_cont_consulta_situacao',
    ),
    path(
        'almoxarifado/cont/entrada-ont-1/',
        views.view_entrada_ont_1,
        name='almoxarifado_cont_entrada_ont_1',
    ),
    path(
        'almoxarifado/cont/entrada-ont-2/',
        views.view_entrada_ont_2,
        name='almoxarifado_cont_entrada_ont_2',
    ),
    path(
        'almoxarifado/cont/entrada-ont-3/',
        views.view_entrada_ont_3,
        name='almoxarifado_cont_entrada_ont_3',
    ),
    path(
        'almoxarifado/cont/saida-ont-1/',
        views.view_saida_ont_1,
        name='almoxarifado_cont_saida_ont_1',
    ),
    path(
        'almoxarifado/cont/saida-ont-2/',
        views.view_saida_ont_2,
        name='almoxarifado_cont_saida_ont_2',
    ),
]
