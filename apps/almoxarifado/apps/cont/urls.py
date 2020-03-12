from django.urls import path

from . import views


urlpatterns = [
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
]
