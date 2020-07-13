from django.urls import path, include

from . import views


urlpatterns = [
    path('', include('apps.almoxarifado.apps.lista_saida.urls')),
    path('', include('apps.almoxarifado.apps.cont.urls')),

    path(
        'almoxarifado/',
        views.index,
        name='almoxarifado_menu_principal',
    ),
    path(
        'almoxarifado/cadastros/',
        views.cadastros,
        name='almoxarifado_menu_cadastros',
    ),
    path(
        'almoxarifado/menu-cadastros/usuario-inativo/<str:callback>',
        views.view_cadastrar_usuario_passivo,
        name='almoxarifado_cadastrar_usuario_passivo_lista',
    ),
    path(
        'almoxarifado/menu-cadastros/usuario-inativo/',
        views.view_cadastrar_usuario_passivo,
        name='almoxarifado_cadastrar_usuario_passivo',
    ),
    path(
        'almoxarifado/cadastros/material/',
        views.cadastra_material,
        name='almoxarifado_cadastrar_material',
    ),
    path(
        'almoxarifado/cadastros/fornecedor/',
        views.cadastra_fornecedor,
        name='almoxarifado_cadastrar_fornecedor',
    ),
    path(
        'almoxarifado/entradas/material/',
        views.entrada_material,
        name='almoxarifado_entrada_material',
    ),
    path(
        'almoxarifado/consultas/',
        views.consultas,
        name='almoxarifado_menu_consultas',
    ),
    path(
        'almoxarifado/consultas/estoque/',
        views.consulta_estoque,
        name='almoxarifado_consulta_estoque',
    ),
    path(
        'almoxarifado/consultas/estoque/<int:material>/',
        views.consulta_estoque_detalhe,
        name='almoxarifado_consulta_estoque_detalhe',
    ),
    path(
        'almoxarifado/consultas/ordens/entradas/',
        views.consulta_ordem_entrada,
        name='almoxarifado_consulta_ordem_entrada',
    ),
    path(
        'almoxarifado/consultas/ordens/saidas/',
        views.consulta_ordem_saida,
        name='almoxarifado_consulta_ordem_saida',
    ),
    path(
        'almoxarifado/consultas/ordens/<int:tipo>/<int:ordem>/',
        views.consulta_ordem_detalhe,
        name='almoxarifado_consulta_ordem_detalhe',
    ),
    path(
        'almoxarifado/consultas/funcionarios/',
        views.consulta_funcionario,
        name='almoxarifado_consulta_funcionario',
    ),
    path(
        'almoxarifado/consultas/funcionarios/<str:funcionario>/',
        views.consulta_funcionario_detalhe,
        name='almoxarifado_consulta_funcionario_detalhe',
    ),
    path(
        'almoxarifado/consultas/funcionarios/<str:funcionario>/<int:ordem>/',
        views.consulta_funcionario_detalhe_ordem,
        name='almoxarifado_consulta_funcionario_detalhe_ordem',
    ),
    path(
        'almoxarifado/consultas/fornecedores/',
        views.consulta_fornecedor,
        name='almoxarifado_consulta_fornecedor',
    ),
    path(
        'almoxarifado/consultas/fornecedores/<int:material>/',
        views.consulta_fornecedor_detalhe,
        name='almoxarifado_consulta_fornecedor_detalhe',
    ),
    path(
        'almoxarifado/consultas/materiais/saidas/',
        views.consulta_material_saida,
        name='almoxarifado_consulta_material_saida',
    ),
    path(
        'almoxarifado/consultas/materiais/saidas/<int:codigo>/',
        views.consulta_material_saida_detalhe,
        name='almoxarifado_consulta_material_saida_detalhe',
    ),
]
