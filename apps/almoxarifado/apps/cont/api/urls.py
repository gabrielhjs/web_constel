from django.urls import path

from . import view_sets


urlpatterns = [
    path(
        'almoxarifado/cont/api/login/',
        view_sets.CreateTokenView.as_view(),
        name='almoxarifado_cont_api_login',
    ),
    path(
        'almoxarifado/cont/api/user/',
        view_sets.ViewUsers.as_view(),
        name='almoxarifado_cont_api_user',
    ),
]
