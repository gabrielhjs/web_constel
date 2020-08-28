from django.urls import path, include

from . import views


urlpatterns = [
    path('', include('apps.almoxarifado.apps.cont.api.urls')),
    path('', include('apps.almoxarifado.apps.cont.api2.urls')),

    path(
        'almoxarifado/cont/',
        views.index,
        name='almoxarifado_cont_menu_principal',
    ),
    path(
        'almoxarifado/cont/cadastros/',
        views.cadastros,
        name='almoxarifado_cont_menu_cadastros',
    ),
    path(
        'almoxarifado/cont/consultas/',
        views.consultas,
        name='almoxarifado_cont_menu_consultas',
    ),
    path(
        'almoxarifado/cont/cadastros/secao/',
        views.cadastrar_secao,
        name='almoxarifado_cont_cadastrar_secao',
    ),
    path(
        'almoxarifado/cont/cadastros/modelo/',
        views.cadastrar_modelo,
        name='almoxarifado_cont_cadastrar_modelo',
    ),
    path(
        'almoxarifado/cont/consultas/situacao/',
        views.consulta_status,
        name='almoxarifado_cont_consulta_situacao',
    ),
    path(
        'almoxarifado/cont/consultas/situacao/<int:status>/<int:secao>/<int:modelo>/',
        views.consulta_status_detalhe,
        name='almoxarifado_cont_consulta_situacao_detalhe',
    ),
    path(
        'almoxarifado/cont/consultas/cargas/',
        views.consulta_tecnicos_carga,
        name='almoxarifado_cont_consulta_tecnicos_carga',
    ),
    path(
        'almoxarifado/cont/consultas/cargas/<str:funcionario>/',
        views.consulta_tecnicos_carga_detalhe,
        name='almoxarifado_cont_consulta_tecnicos_carga_detalhes',
    ),
    path(
        'almoxarifado/cont/consultas/saidas/',
        views.consulta_saidas,
        name='almoxarifado_cont_consulta_saidas',
    ),
    path(
        'almoxarifado/cont/consultas/saidas/<int:ordem>/',
        views.consulta_saidas_detalhe,
        name='almoxarifado_cont_consulta_saidas_detalhes',
    ),
    path(
        'almoxarifado/cont/consultas/devolucoes/',
        views.consulta_devolucoes,
        name='almoxarifado_cont_consulta_devolucoes',
    ),
    path(
        'almoxarifado/cont/consultas/devolucoes/<int:ordem>/',
        views.consulta_devolucoes_detalhe,
        name='almoxarifado_cont_consulta_devolucoes_detalhes',
    ),
    path(
        'almoxarifado/cont/consultas/ont/',
        views.consulta_ont,
        name='almoxarifado_cont_consulta_ont',
    ),
    path(
        'almoxarifado/cont/consultas/ont/<str:serial>/',
        views.consulta_ont_detalhe,
        name='almoxarifado_cont_consulta_ont_detalhe',
    ),
    # path(
    #     'almoxarifado/cont/consultas/dashboard/',
    #     views.consulta_dashboard,
    #     name='almoxarifado_cont_dashboard',
    # ),
    path(
        'almoxarifado/cont/entrada-1/',
        views.entrada_1,
        name='almoxarifado_cont_entrada_ont_1',
    ),
    path(
        'almoxarifado/cont/entrada-2/',
        views.entrada_2,
        name='almoxarifado_cont_entrada_ont_2',
    ),
    path(
        'almoxarifado/cont/entrada-3/',
        views.entrada_3,
        name='almoxarifado_cont_entrada_ont_3',
    ),
    path(
        'almoxarifado/cont/baixa/psw-login',
        views.baixa_login_psw,
        name='almoxarifado_cont_baixa_psw_login',
    ),
    path(
        'almoxarifado/cont/baixa/psw-contrato',
        views.baixa_busca_contrato,
        name='almoxarifado_cont_baixa_psw_contrato',
    ),
    path(
        'almoxarifado/cont/fechamentos',
        views.fechamentos,
        name='almoxarifado_cont_defeito',
    ),
    path(
        'almoxarifado/cont/fechamento/entrada/defeito',
        views.defeito_registra,
        name='almoxarifado_cont_entrada_defeito',
    ),
    path(
        'almoxarifado/cont/fechamento/entrada/defeito/limpa',
        views.defeito_registra_limpa,
        name='almoxarifado_cont_entrada_defeito_limpa',
    ),
    path(
        'almoxarifado/cont/fechamento/entrada/manutencao_1',
        views.manutencao_registra_1,
        name='almoxarifado_cont_entrada_manutencao_1',
    ),
    path(
        'almoxarifado/cont/fechamento/entrada/manutencao_2',
        views.manutencao_registra_2,
        name='almoxarifado_cont_entrada_manutencao_2',
    ),
    path(
        'almoxarifado/cont/fechamento/entrada/manutencao/limpa',
        views.manutencao_registra_limpa,
        name='almoxarifado_cont_entrada_manutencao_limpa',
    ),
]
