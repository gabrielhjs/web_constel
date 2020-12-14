from django.urls import path

from . import views


urlpatterns = [
  path(
    'patrimonio/saidas/lista/',
    views.lista_cria,
    name='patrimonio_saidas_lista_cria',
  ),
  path(
    'patrimonio/saidas/lista/itens/<int:user_to>/',
    views.lista_insere,
    name='patrimonio_saidas_lista_itens',
  ),
  path(
    'patrimonio/saidas/lista/itens/<int:user_to>/ferramenta/',
    views.lista_insere_ferramenta,
    name='patrimonio_saidas_lista_itens_ferramenta',
  ),
  path(
    'patrimonio/saidas/lista/itens/<int:user_to>/patrimonio/',
    views.lista_insere_patrimonio,
    name='patrimonio_saidas_lista_itens_patrimonio',
  ),
  path(
    'patrimonio/saidas/lista/entrega/<int:user_to>/',
    views.lista_entrega,
    name='patrimonio_saidas_lista_entrega',
  ),
  path(
    'patrimonio/saidas/lista/conclui/<int:ordem_id>/',
    views.lista_conclui,
    name='patrimonio_saidas_lista_conclui',
  ),
  path(
    'patrimonio/saidas/lista/imprime/<int:ordem_id>/',
    views.lista_imprime,
    name='patrimonio_saidas_lista_imprime',
  ),
  path(
    'patrimonio/saidas/lista/limpa/<int:user_to>/',
    views.lista_limpa,
    name='patrimonio_saidas_lista_limpa',
  ),
  path(
    'patrimonio/saidas/lista/limpa/<int:user_to>/ferramenta/',
    views.lista_limpa_ferramenta,
    name='patrimonio_saidas_lista_limpa_ferramenta',
  ),
  path(
    'patrimonio/saidas/lista/limpa/<int:user_to>/patrimonio/',
    views.lista_limpa_patrimonio,
    name='patrimonio_saidas_lista_limpa_patrimonio',
  ),
]
