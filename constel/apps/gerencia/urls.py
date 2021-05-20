from django.urls import path

from . import views

urlpatterns = [
    path('gerencia/', views.index, name='constel_gerencia'),
    path('gerencia/painel-diario/', views.painel_diario, name='constel_gerencia_painel_diario'),
]
