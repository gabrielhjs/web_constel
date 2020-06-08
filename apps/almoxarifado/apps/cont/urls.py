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
]
