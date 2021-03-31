from django.urls import path

from . import views


urlpatterns = [
    path(
        'patrimonio/combustivel/cartao/',
        views.index,
        name='patrimonio_combustivel_cartao'
    ),
    path(
        'patrimonio/combustivel/cartao/importar/',
        views.importa_csv,
        name='patrimonio_combustivel_cartao_importa_csv'
    ),
    path(
        'patrimonio/combustivel/cartao/consultas/depositos/',
        views.consulta_depositos,
        name='patrimonio_combustivel_cartao_consulta_depositos'
    ),
    path(
        'patrimonio/combustivel/cartao/consultas/depositos/<int:upload>/',
        views.consulta_depositos_detalhe,
        name='patrimonio_combustivel_cartao_consulta_depositos_detalhe'
    ),
]
