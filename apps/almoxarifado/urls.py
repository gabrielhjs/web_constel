from django.urls import path

from . import views


urlpatterns = [
    path('almoxarifado/', views.view_menu_principal, name='almoxarifado_menu_principal'),
    path('almoxarifado/menu-cadastros/', views.view_menu_cadastros, name='almoxarifado_menu_cadastros'),
    path(
        'almoxarifado/menu-cadastros/material/',
        views.view_cadastrar_material,
        name='almoxarifado_cadastrar_material',
    ),
    path('almoxarifado/menu-consultas/', views.view_menu_consultas, name='almoxarifado_menu_consultas'),
    path(
        'almoxarifado/menu-consultas/materiais/',
        views.ViewConsultaMateriais.as_view(),
        name='almoxarifado_consulta_materiais',
    ),
    path('almoxarifado/menu-relatorios/', views.view_menu_relatorios, name='almoxarifado_menu_relatorios'),
]
