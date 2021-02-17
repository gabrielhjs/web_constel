from django.db import models


class SentinelaContratos(models.Model):
  wfm_id = models.IntegerField(unique=True, null=False)
  sistema_ext_id = models.CharField(null=False, max_length=20)
  contrato = models.CharField(null=False, max_length=15)
  recurso = models.CharField(null=False, max_length=255)
  tipo = models.CharField(null=False, max_length=20)
  status = models.CharField(null=False, max_length=20)
  cidade = models.CharField(null=False, max_length=50)
  porta = models.CharField(null=False, max_length=50)
  porta_n = models.CharField(null=False, max_length=10)
