from django.urls import path

from . import views

urlpatterns = [
    path('acesso-restrito/', views.acesso_negado, name='constel_acesso_restrito'),
    path('administracao/acesso/', views.index, name='constel_acesso_menu_principal'),
    path('administracao/acesso/usuarios/', views.usuarios, name='constel_acesso_usuarios'),
    path('administracao/acesso/usuarios/<str:username>', views.usuarios_grupos, name='constel_acesso_usuarios_grupos'),
    path('administracao/acesso/grupos/', views.grupos, name='constel_acesso_grupos'),
    path('administracao/acesso/grupos/<int:grupo>', views.grupos_usuarios, name='constel_acesso_grupos_usuarios'),
]
