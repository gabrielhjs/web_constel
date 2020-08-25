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

    # Novas urls

    path(
        'patrimonio/cadastros/ferramenta/',
        views.cadastra_ferramenta,
        name='patrimonio_cadastrar_ferramenta',
    ),
    path(
        'patrimonio/entradas/ferramenta/',
        views.entrada_ferramenta,
        name='patrimonio_entrada_ferramenta',
    ),
    path(
        'patrimonio/saidas/ferramenta/',
        views.saida_ferramenta,
        name='patrimonio_saida_ferramenta',
    ),
    path(
        'patrimonio/fechamento/ferramenta/',
        views.fechamento_ferramenta,
        name='patrimonio_fechamento_ferramenta',
    ),
    path(
        'patrimonio/consultas/ferramenta/',
        views.consulta_ferramenta,
        name='patrimonio_consulta_ferramenta',
    ),
    path(
        'patrimonio/consultas/ferramenta/estoque/',
        views.consulta_ferramenta_estoque,
        name='patrimonio_consulta_ferramenta_estoque',
    ),
]
