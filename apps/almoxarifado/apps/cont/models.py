from django.db import models
from django.contrib.auth.models import User


class Modelo(models.Model):
    modelo = models.CharField(unique=True)
    descricao = models.TextField(max_length=500)
    data = models.DateTimeField(auto_now=True)


class Ont(models.Model):
    CHOICES = [
        (0, 'Estoque'),
        (1, 'Campo'),
        (2, 'Aplicada'),
        (3, 'Defeito'),
        (4, 'Devolvida')
    ]
    codigo = models.CharField(max_length=16, min_length=16, null=False, blank=False, unique=True)
    modelo = models.ForeignKey(Modelo, on_delete=models.PROTECT, related_name='modelo')
    status = models.IntegerField(choices=CHOICES)


class Cliente(models.Model):
    contrato = models.IntegerField(null=False, blank=False)
    nome = models.CharField(max_length=255, blank=True, null=True)
    sinal_ont = models.FloatField()
    sinal_olt = models.FloatField()
    ont = models.ForeignKey(Ont, on_delete=models.PROTECT, related_name='cliente_ont')


class OntEntrada(models.Model):
    ont = models.ForeignKey(Ont, on_delete=models.CASCADE, null=False, blank=False, related_name='entrada_ont')
    data = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='entrada_user')


class OntSaida(models.Model):
    ont = models.ForeignKey(Ont, on_delete=models.CASCADE, null=False, blank=False, related_name='saida_ont')
    data = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='saida_user')
    user_to = models.ForeignKey(User, on_delete=models.PROTECT, related_name='saida_user_to')


class OntAplicado(models.Model):
    ont = models.ForeignKey(Ont, on_delete=models.CASCADE, null=False, blank=False, related_name='aplicado_ont')
    data = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='aplicado_user')
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
