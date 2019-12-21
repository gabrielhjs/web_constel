from django.db import models
from django.contrib.auth.models import User

from apps.almoxarifado.models import Material


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
