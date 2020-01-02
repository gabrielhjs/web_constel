from django.urls import path

from . import views


urlpatterns = [
    path(
        'almoxarifado/menu-saidas/lista/',
        views.view_lista_cria,
        name='almoxarifado_saida_lista',
    ),
    path(
        'almoxarifado/menu-saidas/lista/itens/<str:user_to>/',
        views.view_item_insere,
        name='almoxarifado_saida_lista_itens',
    ),
    path(
        'almoxarifado/menu-saidas/lista/itens/entrega/<str:user_to>/',
        views.view_item_entrega,
        name='almoxarifado_saida_lista_itens_entrega',
    ),
    path(
        'almoxarifado/menu-saidas/lista/itens/imprimir/<int:ordem_id>/',
        views.view_item_imprime,
        name='almoxarifado_saida_lista_itens_imprimi',
    ),
    path(
        'almoxarifado/menu-saidas/lista/itens/limpa/<str:user_to>/',
        views.view_item_limpa,
        name='almoxarifado_saida_lista_itens_limpa',
    ),
    path(
        'almoxarifado/menu-saidas/lista/itens/concluido/<int:ordem_id>/',
        views.view_item_conclui,
        name='almoxarifado_saida_lista_itens_conclui',
    ),
]
