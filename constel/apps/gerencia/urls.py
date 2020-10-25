from django.urls import path

from . import views

urlpatterns = [
    path('gerencia/', views.index, name='constel_gerencia'),
]
