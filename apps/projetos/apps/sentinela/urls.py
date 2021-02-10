from django.urls import path, include

from . import views


urlpatterns = [

    path(
        'projetos/sentinela/consulta',
        views.consulta_queue,
        name='sentinela_consulta_queue',
    )
]
