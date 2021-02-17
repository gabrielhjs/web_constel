from django.urls import path, include

from . import views


urlpatterns = [

    path(
        'projetos/sentinela/consulta',
        views.consulta_queue,
        name='sentinela_consulta_queue',
    ),
    path(
        'projetos/sentinela/consulta/contrato',
        views.ViewConsultaNovosContratos.as_view(),
        name='sentinela_consulta_novo_contrato',
    ),
    path(
        'projetos/sentinela/contrato',
        views.ViewInsereNovoContrato.as_view(),
        name='sentinela_insere_contrato',
    ),
]
