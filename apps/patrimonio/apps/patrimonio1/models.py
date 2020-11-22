from django.db import models
from django.contrib.auth.models import User


class Patrimonio(models.Model):
    """
    Model que gerencia a tabela de materiais cadastrados no patrimônio
    """
    nome = models.CharField(max_length=255, verbose_name='Nome')
    descricao = models.TextField(verbose_name='Descrição', max_length=500)
    data = models.DateTimeField(auto_now=True, verbose_name='Data de entrada')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='patrimonios_cadastrados', default=None)
    valor = models.FloatField(null=False, blank=False, default=0)

    def __str__(self):

        return '%s' % self.nome

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class PatrimonioId(models.Model):
    """
    Model que gerencia a tabela de identificação do patrimônio existente
    """
    STATUS = [
        (0, 'Estoque'),
        (1, 'Em uso'),
        (2, 'Defeito'),
        (2, 'Manutenção'),
        (3, 'Inutilizado'),
    ]
    status = models.IntegerField(choices=STATUS, default=0)
    patrimonio = models.ForeignKey(Patrimonio, on_delete=models.CASCADE, related_name='patrimonio_id')
    codigo = models.IntegerField(verbose_name='Código', null=False, blank=False, default=0)

    def __str__(self):

        return '%s | %s' % (self.patrimonio, self.codigo)

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class PatrimonioEntrada1(models.Model):
    """
    Model que gerencia a tabela de entradas de materiais do patrimônio
    """
    patrimonio = models.ForeignKey(PatrimonioId, on_delete=models.CASCADE, related_name='patrimonio_entrada')
    observacao = models.TextField(verbose_name='Observação', max_length=500, null=True, blank=True)
    data = models.DateTimeField(auto_now=True, verbose_name='Data de entrada')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_entrada_patrimonio', default=None)

    def __str__(self):

        return '%s | %s | %.19s' % (self.patrimonio.patrimonio, self.patrimonio.codigo, self.data)

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class PatrimonioEntradaHistorico(models.Model):
    patrimonio = models.ForeignKey(PatrimonioId, on_delete=models.CASCADE, related_name='patrimonio_historico_entrada')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='entrada_historico_patrimonio')

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class PatrimonioSaida(models.Model):
    """
    Model que gerencia a tabela de saídas de materiais do patrimônio
    """
    entrada = models.OneToOneField(
        PatrimonioEntrada1,
        on_delete=models.CASCADE,
        related_name='patrimonio_entrada_saida',
        verbose_name='Patrimônio',
    )
    patrimonio = models.ForeignKey(PatrimonioId, on_delete=models.CASCADE, related_name='patrimonio_saida')
    observacao = models.TextField(verbose_name='Observação', max_length=500, null=True, blank=True)
    data = models.DateTimeField(auto_now=True, verbose_name='Data de saída')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='patrimonio_saidas')
    user_to = models.ForeignKey(User, on_delete=models.PROTECT, related_name='patrimonio_retiradas')

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None
