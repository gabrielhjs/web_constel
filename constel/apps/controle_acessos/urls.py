from django.urls import path

from . import views

urlpatterns = [
    path('menu-admin/controle-acessos/', views.view_menu_controle_acessos, name='constel_menu_controle_acessos'),
    path('menu-admin/controle-acessos/grupos/', views.view_menu_grupos, name='constel_controle_menu_grupos'),
    path('menu-admin/controle-acessos/grupos/criar/', views.view_grupos_criar, name='constel_controle_grupos_criar'),
    path(
        'menu-admin/controle-acessos/grupos/usuarios/',
        views.view_grupos_usuarios,
        name='constel_controle_grupos_usuarios'
    ),
    path(
        'menu-admin/controle-acessos/grupos/usuario/<int:usuario_id>',
        views.view_grupos_usuario,
        name='constel_controle_grupos_usuario'
    ),
    path('authorization-denied/', views.view_acesso_negado, name='constel_acesso_negado'),
]
