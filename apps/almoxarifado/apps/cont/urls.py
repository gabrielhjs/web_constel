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
]
