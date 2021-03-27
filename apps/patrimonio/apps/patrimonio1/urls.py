from django.urls import path

from . import views


urlpatterns = [

    # Novas urls

    path(
        'patrimonio/cadastros/patrimonio/',
        views.cadastra_patrimonio,
        name='patrimonio_cadastrar_patrimonio',
    ),
    path(
        'patrimonio/entradas/patrimonio_1/',
        views.entrada_patrimonio_1,
        name='patrimonio_entrada_patrimonio_1',
    ),
    path(
        'patrimonio/entradas/patrimonio_2/',
        views.entrada_patrimonio_2,
        name='patrimonio_entrada_patrimonio_2',
    ),
    path(
        'patrimonio/entradas/patrimonio_3/',
        views.entrada_patrimonio_3,
        name='patrimonio_entrada_patrimonio_3',
    ),
    path(
        'patrimonio/saidas/patrimonio/',
        views.saida_patrimonio,
        name='patrimonio_saida_patrimonio',
    ),
    path(
        'patrimonio/saidas/patrimonio/conclui/<int:ordem_id>/',
        views.saida_patrimonio_conclui,
        name='patrimonio_saida_patrimonio_conclui',
    ),
    path(
        'patrimonio/saidas/patrimonio/imprime/<int:ordem_id>/',
        views.saida_patrimonio_imprime,
        name='patrimonio_saida_patrimonio_imprime',
    ),
    path(
        'patrimonio/consultas/patrimonio/',
        views.consulta_patrimonio,
        name='patrimonio_consulta_patrimonio',
    ),
    path(
        'patrimonio/consultas/patrimonio/status/',
        views.consulta_patrimonio_status,
        name='patrimonio_consulta_patrimonio_status',
    ),
    path(
        'patrimonio/consultas/patrimonio/status/<int:patrimonio>/',
        views.consulta_patrimonio_status_detalhe,
        name='patrimonio_consulta_patrimonio_status_detalhe',
    ),
    path(
        'patrimonio/edicao/patrimonio/modelo/<int:modelo_id>/',
        views.edita_modelo_patrimonio,
        name='patrimonio_edita_modelo_patrimonio',
    ),
    path(
        'patrimonio/edicao/patrimonio/<int:patrimonio_id>/',
        views.edita_patrimonio,
        name='patrimonio_edita_patrimonio',
    ),
    path(
        'patrimonio/excluir/patrimonio/<int:patrimonio_id>/',
        views.excluir_patrimonio,
        name='patrimonio_excluir_patrimonio',
    ),
]
