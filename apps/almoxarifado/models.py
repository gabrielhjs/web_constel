from django.db import models
from django.contrib.auth.models import User


class Fornecedor(models.Model):
    """
    Model que gerencia a tabela de fornecedores de materiais para o almoxarifado
    """
    nome = models.CharField(verbose_name='Fornecedor', max_length=255, blank=False, unique=True)
    cnpj = models.IntegerField(verbose_name='CNPJ', null=False, blank=False)


class Material(models.Model):
    """
    Model que gerencia a tabela de materiais cadastrados
    """
    codigo = models.IntegerField(verbose_name='Código', null=False, blank=False, unique=True)
    material = models.CharField(max_length=255, verbose_name='Nome')
    descricao = models.CharField(verbose_name='Descrição', max_length=500)
    data = models.DateTimeField(auto_now=True, verbose_name='Data de cadastro')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='materiais_cadastrados', default=None)

    def __str__(self):

        return '%s' % self.material

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class MaterialQuantidade(models.Model):
    """
    Model que gerencia a tabela de controle da quantidade de materiais em estoque
    """
    material = models.OneToOneField(Material, on_delete=models.CASCADE, related_name='quantidade')
    quandidade = models.IntegerField(verbose_name='Quantidade', null=False, blank=False)

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class MaterialEntrada(models.Model):
    """
    Model que gerencia a tabela de entradas de materiais no almoxarifado
    """
    material = models.ForeignKey(Material, on_delete=models.PROTECT, related_name='entradas')
    quantidade = models.IntegerField(verbose_name='Quantidade', null=True, blank=True)
    data = models.DateTimeField(auto_now=True, verbose_name='Data de entrada')
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT, related_name='aquisicoes')

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class MaterialSaida(models.Model):
    """
    Model qeu gerencia a tabela de saídas de materiais do almoxarifado
    """
    material = models.ForeignKey(Material, on_delete=models.PROTECT, related_name='saidas')
    quantidade = models.IntegerField(verbose_name='Quantidade', null=True, blank=True)
    data = models.DateTimeField(auto_now=True, verbose_name='Data de saída')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='retiradas')

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None
