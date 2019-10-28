from django.urls import path

from . import views

urlpatterns = [
    path('gc/cadtalao', views.get_name, name='cadastro_talao'),
    path('gc', views.view_index, name='gc_index'),
    path('gc/contalao', views.view_taloes, name='consulta_talao'),
    path('gc/contalao/<int:talao_id>/', views.view_talao, name='detalhes_talao'),
]
