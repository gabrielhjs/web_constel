from django.urls import path, include

from . import views

urlpatterns = [
    # Includes
    path('', include('apps.web_gc.urls')),

    # Constel urls
    path('cadusuario', views.view_cadastrar_usuario, name='cadastra_usuario'),
    path('cadusuario-pass', views.view_cadastrar_usuario_passivo, name='cadastra_usuario_passivo'),
    path('cadveiculo', views.view_cadastrar_veiculo, name='cadastra_veiculo'),
    path('login', views.view_login, name='login'),
    path('logout', views.view_logout, name='logout'),
    path('', views.index, name='index'),
]
