from django.urls import path

from . import views

urlpatterns = [
    path('cadusuario/', views.view_cadastrar_usuario, name='cadastra_usuario'),
    path('cadusuario-pass/', views.view_cadastrar_usuario_passivo, name='cadastra_usuario_passivo'),
    path('cadveiculo/', views.view_cadastrar_veiculo, name='cadastra_veiculo'),
    path('login/', views.view_login, name='login'),
    path('logout/', views.view_logout, name='logout'),
    path('', views.index, name='index'),
    path('menu-admin/', views.view_menu_gerenciamento_sistema, name='constel_menu_admin'),
    path('menu-admin/view-admin/', views.view_admin, name='constel_view_admin'),
    path('menu-admin/controle-acessos/', views.view_controle_acessos, name='constel_controle_acessos'),
    path('consulta/usuarios/', views.view_consulta_funcionarios, name='consulta_funcionarios'),
    path('consulta/veiculos/', views.view_consulta_veiculos, name='consulta_veiculos'),
]
