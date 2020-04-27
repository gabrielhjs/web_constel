from django.urls import path

from . import views, views_ont


urlpatterns = [
    path(
        'almoxarifado/saidas/material/lista/',
        views.lista_cria,
        name='almoxarifado_saida_lista',
    ),
    path(
        'almoxarifado/saidas/material/lista/itens/<str:user_to>/',
        views.lista_insere,
        name='almoxarifado_saida_lista_itens',
    ),
    path(
        'almoxarifado/saidas/material/lista/entrega/<str:user_to>/',
        views.lista_entrega,
        name='almoxarifado_saida_lista_entrega',
    ),
    path(
        'almoxarifado/saidas/material/lista/imprimi/<int:ordem_id>/',
        views.lista_imprime,
        name='almoxarifado_saida_lista_imprimi',
    ),
    path(
        'almoxarifado/saidas/material/lista/limpa/<str:user_to>/',
        views.lista_limpa,
        name='almoxarifado_saida_lista_limpa',
    ),
    path(
        'almoxarifado/saidas/material/lista/conclui/<int:ordem_id>/',
        views.lista_conclui,
        name='almoxarifado_saida_lista_conclui',
    ),

    # Urls das listas de saída de Ont

    path(
        'almoxarifado/cont/menu-saidas/lista/',
        views_ont.view_lista_cria,
        name='almoxarifado_cont_saida_lista',
    ),
    path(
        'almoxarifado/cont/menu-saidas/lista/itens/<str:user_to>/',
        views_ont.view_item_insere,
        name='almoxarifado_cont_saida_lista_itens',
    ),
    path(
        'almoxarifado/cont/menu-saidas/lista/itens/entrega/<str:user_to>/',
        views_ont.view_item_entrega,
        name='almoxarifado_cont_saida_lista_itens_entrega',
    ),
    path(
        'almoxarifado/cont/menu-saidas/lista/itens/imprimir/<int:ordem_id>/',
        views_ont.view_item_imprime,
        name='almoxarifado_cont_saida_lista_itens_imprimi',
    ),
    path(
        'almoxarifado/cont/menu-saidas/lista/itens/limpa/<str:user_to>/',
        views_ont.view_item_limpa,
        name='almoxarifado_cont_saida_lista_itens_limpa',
    ),
    path(
        'almoxarifado/cont/menu-saidas/lista/itens/concluido/<int:ordem_id>/',
        views_ont.view_item_conclui,
        name='almoxarifado_cont_saida_lista_itens_conclui',
    ),
]
