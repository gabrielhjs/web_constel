from django.urls import path, include

from . import views

urlpatterns = [
    path('', include('constel.apps.controle_acessos.urls')),

    path('cadusuario/', views.view_cadastrar_usuario, name='cadastra_usuario'),
    # path('cadusuario-pass/', views.view_cadastrar_usuario_passivo, name='cadastra_usuario_passivo'),
    # path('cadveiculo/', views.view_cadastrar_veiculo, name='cadastra_veiculo'),
    path('login/', views.view_login, name='login'),
    path('logout/', views.view_logout, name='logout'),
    path('', views.indexv2, name='index'),
    path('administracao/', views.admin, name='constel_admin'),
    path('consulta/usuarios/next=<str:rollback>', views.view_consulta_funcionarios, name='consulta_funcionarios'),
    path('consulta/veiculos/next=<str:rollback>', views.view_consulta_veiculos, name='consulta_veiculos'),
]
