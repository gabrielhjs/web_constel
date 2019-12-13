from django.urls import path

from . import views


urlpatterns = [
    path(
        'patrimonio/combustivel/menu-cadastros/cadastro-talao/',
        views.view_cadastrar_talao,
        name='gc_cadastro_talao'
    ),
    path(
        'patrimonio/combustivel/menu-cadastros/cadastro-combustivel/',
        views.view_cadastrar_combustivel,
        name='gc_cadastro_combustivel'
    ),
    path(
        'patrimonio/combustivel/menu-cadastros/cadastro-posto/',
        views.view_cadastrar_posto,
        name='gc_cadastro_posto'
    ),
    path(
        'patrimonio/combustivel/menu-consultas/consulta-taloes/',
        views.view_taloes,
        name='gc_consulta_taloes',
    ),
    path(
        'patrimonio/combustivel/menu-consultas/consulta-taloes/talao=<int:talao_id>/',
        views.view_talao,
        name='gc_consulta_talao'
    ),
    path(
        'patrimonio/combustivel/menu-consultas/consulta-vales/',
        views.view_vales,
        name='gc_consulta_vales'
    ),
    path(
        'patrimonio/combustivel/menu-consultas/consulta-meus-vales/',
        views.view_meus_vales,
        name='gc_consulta_meus_vales'
    ),
    path(
        'patrimonio/combustivel/menu-relatorios/mensal',
        views.view_relatorio_mensal,
        name='gc_relatorio_mensal'
    ),
    path(
        'patrimonio/combustivel/menu-taloes/entrega-talao/',
        views.view_entrega_talao,
        name='gc_entrega_talao'
    ),
    path(
        'patrimonio/combustivel/menu-vales/entrega-vale-1/',
        views.view_entrega_vale_1,
        name='gc_entrega_vale_1'
    ),
    path(
        'patrimonio/combustivel/menu-vales/entrega-vale-2/',
        views.view_entrega_vale_2,
        name='gc_entrega_vale_2'
    ),
]
