from django.urls import path

from . import views

urlpatterns = [
    path('gc/cadtalao', views.view_cadastrar_talao, name='cadastro_talao'),
    path('gc/enttalao', views.view_entrega_talao, name='entrega_talao'),
    path('gc/entvale', views.view_entrega_vale, name='entrega_vale'),
    path('gc', views.view_index, name='gc_index'),
    path('gc/contalao', views.view_taloes, name='consulta_talao'),
    path('gc/contalao/<int:talao_id>', views.view_talao, name='detalhes_talao'),
]
