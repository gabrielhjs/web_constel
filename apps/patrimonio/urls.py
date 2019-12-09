from django.urls import path

from . import views


urlpatterns = [
    path('patrimonio/', views.view_menu_principal, name='patrimonio_menu_principal'),
    path('patrimonio/menu-cadastros/', views.view_menu_cadastros, name='patrimonio_menu_cadastros'),
    path(
        'patrimonio/menu-cadastros/ferramenta/',
        views.view_cadastrar_ferramenta,
        name='patrimonio_cadastrar_ferramenta',
    ),
    path('patrimonio/menu-consultas/', views.view_menu_consultas, name='patrimonio_menu_consultas'),
    path(
        'patrimonio/menu-consultas/ferramenta/',
        views.ViewConsultaFerramentas.as_view(),
        name='patrimonio_consulta_ferramentas',
    ),
    path('patrimonio/menu-relatorios/', views.view_menu_relatorios, name='patrimonio_menu_relatorios'),
]
