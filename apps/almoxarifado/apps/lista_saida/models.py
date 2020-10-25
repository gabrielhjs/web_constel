from django.db import models
from django.contrib.auth.models import User

from apps.almoxarifado.models import Material, Fornecedor
from ..cont.models import Ont


class Lista(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='lista_saida')
    user_to = models.OneToOneField(User, on_delete=models.PROTECT, related_name='lista_retirada')
    data = models.DateTimeField(auto_now=True, verbose_name='Lista criada em')

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class Item(models.Model):
    lista = models.ForeignKey(Lista, on_delete=models.CASCADE, related_name='lista_itens')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='material_listas')
    quantidade = models.IntegerField(default=1)

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class ListaAgendamento(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='lista_agendamento_saida')
    user_request = models.OneToOneField(User, on_delete=models.PROTECT, related_name='lista_agendamento_retirada')
    data = models.DateTimeField(auto_now=True, verbose_name='Lista criada em')

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class ItemAgendamento(models.Model):
    lista = models.ForeignKey(Lista, on_delete=models.CASCADE, related_name='lista_agendamento_itens')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='material_agendamento_listas')
    quantidade = models.IntegerField(default=1)

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class OntLista(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='cont_lista_saida')
    user_to = models.OneToOneField(User, on_delete=models.PROTECT, related_name='cont_lista_retirada')
    data = models.DateTimeField(auto_now=True, verbose_name='Lista criada em')

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class OntItem(models.Model):
    lista = models.ForeignKey(OntLista, on_delete=models.CASCADE, related_name='cont_lista_itens')
    material = models.ForeignKey(Ont, on_delete=models.CASCADE, related_name='cont_material_listas')

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class DefeitoOntLista(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='cont_defeito_lista_saida')
    fornecedor = models.OneToOneField(Fornecedor, on_delete=models.PROTECT, related_name='cont_defeito_lista_retirada')
    data = models.DateTimeField(auto_now=True, verbose_name='Lista criada em')

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class DefeitoOntItem(models.Model):
    lista = models.ForeignKey(DefeitoOntLista, on_delete=models.CASCADE, related_name='cont_defeito_lista_itens')
    material = models.ForeignKey(Ont, on_delete=models.CASCADE, related_name='cont_defeito_material_listas')

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class ManutencaoOntLista(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='cont_manutencao_lista_saida')
    fornecedor = models.OneToOneField(
        Fornecedor,
        on_delete=models.PROTECT,
        related_name='cont_manutencao_lista_retirada'
    )
    data = models.DateTimeField(auto_now=True, verbose_name='Lista criada em')

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class ManutencaoOntItem(models.Model):
    lista = models.ForeignKey(ManutencaoOntLista, on_delete=models.CASCADE, related_name='cont_manutencao_lista_itens')
    material = models.ForeignKey(Ont, on_delete=models.CASCADE, related_name='cont_manutencao_material_listas')

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None
