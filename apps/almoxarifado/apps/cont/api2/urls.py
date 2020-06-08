from django.urls import path

from . import views


urlpatterns = [
    path(
        'almoxarifado/cont/api2/contrato/',
        views.ViewContrato.as_view(),
        name='almoxarifado_cont_api2_contrato',
    ),
]
