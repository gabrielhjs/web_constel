from django.urls import path

from . import views

urlpatterns = [
    path('gc/cadtalao', views.get_name, name='cadastro_talao'),
    path('gc', views.view_index, name='gc_index'),
]
