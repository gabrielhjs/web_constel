from django.db import models
from django.contrib.auth.models import User

from ...models import Ordem, Fornecedor


class Modelo(models.Model):
    nome = models.CharField(max_length=255, unique=True)
    descricao = models.TextField(max_length=500)
    data = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class Secao(models.Model):
    nome = models.CharField(max_length=255, unique=True)
    descricao = models.TextField(max_length=500)
    data = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class Ont(models.Model):
    CHOICES = [
        (0, 'Estoque'),
        (1, 'Campo'),
        (2, 'Aplicada'),
        (3, 'Defeito'),
        (4, 'Devolvida'),
        (4, 'Retirada'),
    ]
    codigo = models.CharField(max_length=20, null=False, blank=False, unique=True, )
    modelo = models.ForeignKey(Modelo, on_delete=models.PROTECT, related_name='ont_modelo')
    secao = models.ForeignKey(Secao, on_delete=models.PROTECT, related_name='ont_secao')
    status = models.IntegerField(choices=CHOICES, editable=False, default=0, )

    def __str__(self):
        return self.codigo

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class Cliente(models.Model):
    porta = models.CharField(max_length=255, default='vazio')
    estado_link = models.CharField(max_length=255, default='vazio')
    nivel_ont = models.FloatField(default=0)
    nivel_olt = models.FloatField(default=0)
    nivel_olt_tx = models.FloatField(default=0)
    ont = models.ForeignKey(Ont, on_delete=models.PROTECT, related_name='cliente_ont')
    contrato = models.IntegerField(null=False, blank=False, default=0)

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class OntEntrada(models.Model):
    ont = models.ForeignKey(Ont, on_delete=models.CASCADE, null=False, blank=False, related_name='entrada_ont')
    data = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='entrada_user')

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class OntEntradaHistorico(models.Model):
    ont = models.ForeignKey(Ont, on_delete=models.CASCADE, null=False, blank=False, related_name='historico_ont')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='entrada_historico_ont')

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class OntSaida(models.Model):
    ordem = models.ForeignKey(Ordem, on_delete=models.CASCADE, default=None, related_name='saida_ordem_ont', null=True)
    entrada = models.ForeignKey(OntEntrada, on_delete=models.CASCADE, default=None, related_name='saida_entrada_ont')
    ont = models.ForeignKey(Ont, on_delete=models.CASCADE, null=False, blank=False, related_name='saida_ont')
    data = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='saida_user')
    user_to = models.ForeignKey(User, on_delete=models.PROTECT, related_name='saida_user_to')

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class OntAplicado(models.Model):
    saida = models.ForeignKey(OntSaida, on_delete=models.CASCADE, default=None, related_name='aplicado_saida_ont')
    data = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='aplicado_user')
    ont = models.ForeignKey(Ont, on_delete=models.CASCADE, null=False, blank=False, related_name='aplicado_ont')
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='aplicado_cliente')

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class OntDefeito(models.Model):
    ont = models.ForeignKey(Ont, on_delete=models.CASCADE, null=False, blank=False, related_name='defeito_ont')
    data = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='dfeito_user')

    # Default fields (apenas para não gerar alertas na IDE)
    # objects = None


class OntDefeitoDevolucao(models.Model):
    ordem = models.ForeignKey(
        Ordem,
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        related_name='devolucao_ordem_ont',
        null=True
    )
    defeito = models.ForeignKey(OntDefeito, on_delete=models.CASCADE, default=None, related_name='devolucao_defeito')
    data = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='devolucao_user')
    ont = models.ForeignKey(Ont, on_delete=models.CASCADE, null=False, blank=False, related_name='devolucao_ont')
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT, related_name='devolucao_fornecedor')

    # Default fields (apenas para não gerar alertas na IDE)
    # objects = None


class OntDefeitoHistorico(models.Model):
    ont = models.ForeignKey(
        Ont,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='historico_ont_defeito'
    )

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='defeito_historico_ont')

    # Default fields (apenas para não gerar alertas na IDE)
    # objects = None
