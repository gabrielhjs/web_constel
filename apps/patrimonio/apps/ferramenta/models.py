from django.db import models
from django.contrib.auth.models import User


class Ferramenta(models.Model):
    """
    Model que gerencia a tabela de ferramentas cadastradas
    """
    nome = models.CharField(max_length=255, verbose_name='Nome')
    descricao = models.TextField(verbose_name='Descrição', max_length=500)
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
    ferramenta = models.OneToOneField(Ferramenta, on_delete=models.CASCADE, related_name='quantidade', editable=False)
    quantidade = models.IntegerField(verbose_name='Quantidade', default=0, editable=False)

    def __str__(self):

        return '%s' % self.ferramenta

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class FerramentaEntrada(models.Model):
    """
    Model que gerencia a tabela de entradas de ferramentas no patrimio
    """
    ferramenta = models.ForeignKey(Ferramenta, on_delete=models.CASCADE, related_name='entradas')
    quantidade = models.IntegerField(verbose_name='Quantidade', null=True, blank=True)
    data = models.DateTimeField(auto_now=True, verbose_name='Data de entrada')
    valor = models.FloatField(null=False, blank=False, default=0, verbose_name='Valor total')
    observacao = models.TextField(verbose_name='Observação', max_length=500, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='ferramentas_entradas', default=None)

    def __str__(self):

        return '%s | %s | %.19s' % (self.ferramenta, self.quantidade, self.data)

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class FerramentaSaida(models.Model):
    """
    Model que gerencia a tabela de saídas de ferramentas no patrimio
    """
    ferramenta = models.ForeignKey(Ferramenta, on_delete=models.CASCADE, related_name='saidas')
    quantidade = models.IntegerField(verbose_name='Quantidade', null=True, blank=True)
    data = models.DateTimeField(auto_now=True, verbose_name='Data de saída')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='saidas')
    user_to = models.ForeignKey(User, on_delete=models.PROTECT, related_name='retiradas')
    observacao = models.TextField(verbose_name='Observação', max_length=500, null=True, blank=True)

    def __str__(self):

        return '%s' % self.ferramenta

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None
