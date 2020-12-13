from django.db import models
from django.contrib.auth.models import User

from ..ferramenta.models import Ferramenta
from ..patrimonio1.models import PatrimonioId


class Lista(models.Model):
  objects = models.manager.Manager

  user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user_patrimonio_lista")
  user_to = models.OneToOneField(User, on_delete=models.PROTECT, related_name="user_to_patrimonio_lista")
  data = models.DateTimeField(auto_now=True, verbose_name="Lista criada em")


class ItemFerramenta(models.Model):
  objects = models.manager.Manager

  lista = models.ForeignKey(Lista, on_delete=models.CASCADE, related_name='lista_ferramentas')
  ferramenta = models.ForeignKey(Ferramenta, on_delete=models.PROTECT)
  quantidade = models.IntegerField(default=1)


class ItemPatrimonio(models.Model):
  objects = models.manager.Manager

  lista = models.ForeignKey(Lista, on_delete=models.CASCADE, related_name='lista_patrimonios')
  patrimonio = models.ForeignKey(PatrimonioId, on_delete=models.PROTECT)
