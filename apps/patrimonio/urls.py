from django.urls import path, include

from . import views


urlpatterns = [
    # Apps
    path('', include('apps.patrimonio.apps.ferramenta.urls')),
    path('', include('apps.patrimonio.apps.patrimonio1.urls')),
    path('', include('apps.patrimonio.apps.combustivel.urls')),
    path('', include('apps.patrimonio.apps.lista_saida_patrimonio.urls')),

    path(
        'patrimonio/',
        views.index,
        name='patrimonio_menu_principal',
    ),
    path(
        'patrimonio/cadastros/',
        views.cadastros,
        name='patrimonio_menu_cadastros',
    ),
    path(
        'patrimonio/entradas/',
        views.entradas,
        name='patrimonio_menu_entradas',
    ),
    path(
        'patrimonio/saidas/',
        views.saidas,
        name='patrimonio_menu_saidas',
    ),
    path(
        'patrimonio/consultas/',
        views.consultas,
        name='patrimonio_menu_consultas',
    ),
    path(
        'patrimonio/consultas/modelos/',
        views.consultas_modelos,
        name='patrimonio_menu_consultas_modelos',
    ),
    path(
        'patrimonio/consultas/saidas/',
        views.consultas_ordem_saida,
        name='patrimonio_consultas_ordem_saida',
    ),
    path(
        'patrimonio/consultas/saidas/<int:ordem>',
        views.consultas_ordem_saida_detalhe,
        name='patrimonio_consultas_ordem_saida_detalhe',
    ),
    path(
        'patrimonio/consultas/colaboradores/',
        views.consulta_colaboradores,
        name='patrimonio_consulta_colaboradores',
    ),
    path(
        'patrimonio/consultas/colaboradores/<str:user>/',
        views.consulta_colaboradores_detalhes,
        name='patrimonio_consulta_colaboradores_detalhes',
    ),
]
