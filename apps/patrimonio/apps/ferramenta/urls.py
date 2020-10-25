from django.urls import path

from . import views


urlpatterns = [
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
    path(
        'patrimonio/edicao/ferramenta/modelo/<int:modelo_id>/',
        views.edita_modelo_ferramenta,
        name='patrimonio_edita_modelo_ferramenta',
    ),
]
