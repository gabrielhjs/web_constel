from django.urls import path, include

from . import views


urlpatterns = [
    # Apps
    path('', include('apps.patrimonio.apps.ferramenta.urls')),
    path('', include('apps.patrimonio.apps.patrimonio1.urls')),
    path('', include('apps.patrimonio.apps.combustivel.urls')),


    path(
        'patrimonio/',
        views.view_menu_principal,
        name='patrimonio_menu_principal',
    ),
    path(
        'patrimonio/menu-cadastros/',
        views.view_menu_cadastros,
        name='patrimonio_menu_cadastros',
    ),
    path(
        'patrimonio/menu-entradas/',
        views.view_menu_entradas,
        name='patrimonio_menu_entradas',
    ),
    path(
        'patrimonio/menu-saidas/',
        views.view_menu_saidas,
        name='patrimonio_menu_saidas',
    ),
    path(
        'patrimonio/menu-consultas/',
        views.view_menu_consultas,
        name='patrimonio_menu_consultas',
    ),
    path(
        'patrimonio/menu-relatorios/',
        views.view_menu_relatorios,
        name='patrimonio_menu_relatorios',
    ),
]
