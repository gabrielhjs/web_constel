from django.urls import path

from . import views, views_ont, views_ont_defeito, views_ont_manutencao


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
        'almoxarifado/cont/saidas/lista/',
        views_ont.lista_cria,
        name='almoxarifado_cont_saida_lista',
    ),
    path(
        'almoxarifado/cont/saidas/lista/<str:user_to>/',
        views_ont.view_insere,
        name='almoxarifado_cont_saida_lista',
    ),
    path(
        'almoxarifado/cont/saidas/lista/entrega/<str:user_to>/',
        views_ont.view_entrega,
        name='almoxarifado_cont_saida_lista_entrega',
    ),
    path(
        'almoxarifado/cont/menu-saidas/lista/imprimir/<int:ordem_id>/',
        views_ont.view_imprime,
        name='almoxarifado_cont_saida_lista_imprimi',
    ),
    path(
        'almoxarifado/cont/menu-saidas/lista/limpa/<str:user_to>/',
        views_ont.view_limpa,
        name='almoxarifado_cont_saida_lista_limpa',
    ),
    path(
        'almoxarifado/cont/saidas/lista/conclui/<int:ordem_id>/',
        views_ont.view_conclui,
        name='almoxarifado_cont_saida_lista_conclui',
    ),

    # Urls das listas de devolução de Ont com defeito

    path(
        'almoxarifado/cont/defeito/saidas/lista/',
        views_ont_defeito.lista_cria,
        name='almoxarifado_cont_defeito_saida_lista',
    ),
    path(
        'almoxarifado/cont/defeito/saidas/lista/<int:fornecedor>/',
        views_ont_defeito.view_insere,
        name='almoxarifado_cont_defeito_saida_lista',
    ),
    path(
        'almoxarifado/cont/defeito/saidas/lista/entrega/<int:fornecedor>/',
        views_ont_defeito.view_entrega,
        name='almoxarifado_cont_defeito_saida_lista_entrega',
    ),
    path(
        'almoxarifado/cont/defeito/saidas/lista/imprimir/<int:ordem_id>/',
        views_ont_defeito.view_imprime,
        name='almoxarifado_cont_defeito_saida_lista_imprimi',
    ),
    path(
        'almoxarifado/cont/defeito/saidas/lista/limpa/<int:fornecedor>/',
        views_ont_defeito.view_limpa,
        name='almoxarifado_cont_defeito_saida_lista_limpa',
    ),
    path(
        'almoxarifado/cont/defeito/saidas/conclui/<int:ordem_id>/',
        views_ont_defeito.view_conclui,
        name='almoxarifado_cont_defeito_saida_lista_conclui',
    ),

    # Urls das listas de devolução de Ont de manutenção

    path(
        'almoxarifado/cont/manutencao/saidas/lista/',
        views_ont_manutencao.lista_cria,
        name='almoxarifado_cont_manutencao_saida_lista',
    ),
    path(
        'almoxarifado/cont/manutencao/saidas/lista/<int:fornecedor>/',
        views_ont_manutencao.view_insere,
        name='almoxarifado_cont_manutencao_saida_lista',
    ),
    path(
        'almoxarifado/cont/manutencao/saidas/lista/entrega/<int:fornecedor>/',
        views_ont_manutencao.view_entrega,
        name='almoxarifado_cont_manutencao_saida_lista_entrega',
    ),
    path(
        'almoxarifado/cont/manutencao/saidas/lista/imprimir/<int:ordem_id>/',
        views_ont_manutencao.view_imprime,
        name='almoxarifado_cont_manutencao_saida_lista_imprimi',
    ),
    path(
        'almoxarifado/cont/manutencao/saidas/lista/limpa/<int:fornecedor>/',
        views_ont_manutencao.view_limpa,
        name='almoxarifado_cont_manutencao_saida_lista_limpa',
    ),
    path(
        'almoxarifado/cont/manutencao/saidas/conclui/<int:ordem_id>/',
        views_ont_manutencao.view_conclui,
        name='almoxarifado_cont_manutencao_saida_lista_conclui',
    ),
]
