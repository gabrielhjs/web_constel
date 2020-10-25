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
        'patrimonio/entradas/patrimonio_1',
        views.entrada_patrimonio_1,
        name='patrimonio_entrada_patrimonio_1',
    ),
    path(
        'patrimonio/entradas/patrimonio_2',
        views.entrada_patrimonio_2,
        name='patrimonio_entrada_patrimonio_2',
    ),
    path(
        'patrimonio/saidas/patrimonio/',
        views.saida_patrimonio,
        name='patrimonio_saida_patrimonio',
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
]
