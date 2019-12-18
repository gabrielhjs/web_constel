from django.urls import path

from . import views


urlpatterns = [
    path(
        'patrimonio/menu-cadastros/ferramenta/',
        views.view_cadastrar_ferramenta,
        name='patrimonio_cadastrar_ferramenta',
    ),
    path(
        'patrimonio/menu-entradas/ferramentas/',
        views.view_entrada_ferramenta,
        name='patrimonio_entrada_ferramenta',
    ),
    path(
        'patrimonio/menu-saidas/ferramentas/',
        views.view_saida_ferramenta,
        name='patrimonio_saida_ferramenta',
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
]
