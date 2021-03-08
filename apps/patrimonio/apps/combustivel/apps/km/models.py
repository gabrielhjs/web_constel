from django.contrib.auth.models import User
from django.db import models


class _Km(models.Model):
  objects: models.manager.Manager

  km = models.FloatField(null=False)
  user = models.ForeignKey(User, on_delete=models.PROTECT, null=False)
  user_to = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
  date = models.DateField(auto_now_add=True)

  class Meta:
    abstract = True


class KmInicial(_Km):
  pass


class KmFinal(_Km):
  km_inicial = models.OneToOneField(KmInicial, on_delete=models.CASCADE)
