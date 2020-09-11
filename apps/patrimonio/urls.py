from django.urls import path, include

from . import views


urlpatterns = [
    # Apps
    path('', include('apps.patrimonio.apps.ferramenta.urls')),
    path('', include('apps.patrimonio.apps.patrimonio1.urls')),
    path('', include('apps.patrimonio.apps.combustivel.urls')),

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
]
