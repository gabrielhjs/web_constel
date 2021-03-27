from django.urls import path, include

from . import views

urlpatterns = [
    # Apps
    path('', include('apps.patrimonio.apps.combustivel.apps.talao.urls')),
    path('', include('apps.patrimonio.apps.combustivel.apps.km.urls')),

    path('patrimonio/combustivel/', views.view_menu_principal, name='gc_menu_principal'),
    path('patrimonio/combustivel/menu-cadastros/', views.view_menu_cadastros, name='gc_menu_cadastros'),
    path('patrimonio/combustivel/menu-consultas/', views.view_menu_consultas, name='gc_menu_consultas'),
    path('patrimonio/combustivel/menu-relatorios/', views.view_menu_relatorios, name='gc_menu_relatorios'),
    path('patrimonio/combustivel/menu-taloes/', views.view_menu_taloes, name='gc_menu_taloes'),
    path('patrimonio/combustivel/menu-vales/', views.view_menu_vales, name='gc_menu_vales'),

]
