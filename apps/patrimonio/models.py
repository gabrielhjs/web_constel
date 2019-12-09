from django.db import models
from django.contrib.auth.models import User


class Patrimonio(models.Model):
    """
    Model que gerencia a tabela de materiais cadastrados no patrimônio
    """
    codigo = models.IntegerField(verbose_name='Código', null=False, blank=False, unique=True)
    nome = models.CharField(max_length=255, verbose_name='Nome')
    descricao = models.CharField(verbose_name='Descrição', max_length=500)

    def __str__(self):

        return '%s' % self.nome

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class PatrimonioEntrada(models.Model):
    """
    Model que gerencia a tabela de entradas de materiais do patrimônio
    """
    patrimonio = models.ForeignKey(Patrimonio, on_delete=models.CASCADE, related_name='entrada')
    data = models.DateTimeField(auto_now=True, verbose_name='Data de entrada')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='entrada_patrimonio', default=None)

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class PatrimonioSaida(models.Model):
    """
    Model qeu gerencia a tabela de saídas de materiais do patrimônio
    """
    entrada = models.OneToOneField(PatrimonioEntrada, on_delete=models.CASCADE, related_name='entrada_saida')
    patrimonio = models.ForeignKey(Patrimonio, on_delete=models.CASCADE, related_name='patrimonio_saida')
    data = models.DateTimeField(auto_now=True, verbose_name='Data de saída')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='patrimonio_saidas')
    user_to = models.ForeignKey(User, on_delete=models.PROTECT, related_name='patrimonio_retiradas')

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class Ferramenta(models.Model):
    """
    Model que gerencia a tabela de ferramentas cadastradas
    """
    nome = models.CharField(max_length=255, verbose_name='Nome')
    descricao = models.CharField(verbose_name='Descrição', max_length=500)
    data = models.DateTimeField(auto_now=True, verbose_name='Data de cadastro')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='ferramentas_cadastradas', default=None)

    def __str__(self):

        return '%s' % self.nome

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class FerramentaQuantidade(models.Model):
    """
    Model que gerencia a tabela de controle da quantidade de ferramentas no patrimônio
    """
    ferramenta = models.OneToOneField(Ferramenta, on_delete=models.CASCADE, related_name='quantidade')
    quandidade = models.IntegerField(verbose_name='Quantidade', null=False, blank=False)

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class FerramentaEntrada(models.Model):
    """
    Model que gerencia a tabela de entradas de ferramentas no patrimio
    """
    ferramenta = models.ForeignKey(Ferramenta, on_delete=models.PROTECT, related_name='entradas')
    quantidade = models.IntegerField(verbose_name='Quantidade', null=True, blank=True)
    data = models.DateTimeField(auto_now=True, verbose_name='Data de entrada')

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class FerramentaSaida(models.Model):
    """
    Model que gerencia a tabela de saídas de ferramentas no patrimio
    """
    ferramenta = models.ForeignKey(Ferramenta, on_delete=models.PROTECT, related_name='saidas')
    quantidade = models.IntegerField(verbose_name='Quantidade', null=True, blank=True)
    data = models.DateTimeField(auto_now=True, verbose_name='Data de saída')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='saidas')
    user_to = models.ForeignKey(User, on_delete=models.PROTECT, related_name='retiradas')

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None
