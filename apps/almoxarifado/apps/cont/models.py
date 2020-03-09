from django.db import models
from django.contrib.auth.models import User


class Modelo(models.Model):
    nome = models.CharField(max_length=255, unique=True, verbose_name='Código')
    descricao = models.TextField(max_length=500)
    data = models.DateTimeField(auto_now=True)

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class Secao(models.Model):
    nome = models.CharField(max_length=255, unique=True)
    descricao = models.TextField(max_length=500)
    data = models.DateTimeField(auto_now=True)

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class Ont(models.Model):
    CHOICES = [
        (0, 'Estoque'),
        (1, 'Campo'),
        (2, 'Aplicada'),
        (3, 'Defeito'),
        (4, 'Devolvida'),
    ]
    codigo = models.CharField(max_length=20, null=False, blank=False, unique=True, )
    modelo = models.ForeignKey(Modelo, on_delete=models.PROTECT, related_name='ont_modelo')
    projeto = models.ForeignKey(Secao, on_delete=models.PROTECT, related_name='ont_secao')
    status = models.IntegerField(choices=CHOICES, editable=False, default=0, )

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class Cliente(models.Model):
    contrato = models.IntegerField(null=False, blank=False)
    nome = models.CharField(max_length=255, blank=True, null=True)
    sinal_ont = models.FloatField()
    sinal_olt = models.FloatField()
    ont = models.ForeignKey(Ont, on_delete=models.PROTECT, related_name='cliente_ont')

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class OntEntrada(models.Model):
    ont = models.ForeignKey(Ont, on_delete=models.CASCADE, null=False, blank=False, related_name='entrada_ont')
    data = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='entrada_user')

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class OntSaida(models.Model):
    entrada = models.ForeignKey(OntEntrada, on_delete=models.CASCADE, default=None, related_name='saida_entrada_ont')
    ont = models.ForeignKey(Ont, on_delete=models.CASCADE, null=False, blank=False, related_name='saida_ont')
    data = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='saida_user')
    user_to = models.ForeignKey(User, on_delete=models.PROTECT, related_name='saida_user_to')

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class OntAplicado(models.Model):
    saida = models.ForeignKey(OntSaida, on_delete=models.CASCADE, default=None, related_name='aplicado_saida_ont')
    ont = models.ForeignKey(Ont, on_delete=models.CASCADE, null=False, blank=False, related_name='aplicado_ont')
    data = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='aplicado_user')
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None
