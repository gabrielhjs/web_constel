from django.db import models
from django.contrib.auth.models import User


class Fornecedor(models.Model):
    """
    Model que gerencia a tabela de fornecedores de materiais para o almoxarifado
    """
    nome = models.CharField(verbose_name='Fornecedor', max_length=255, blank=False, unique=True)
    cnpj = models.BigIntegerField(verbose_name='CNPJ', null=False, blank=False)

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None

    def __str__(self):

        return '%s | %s' % (self.cnpj, self.nome)


class Material(models.Model):
    """
    Model que gerencia a tabela de materiais cadastrados
    """
    TIPOS = [
        (0, 'peça(s)'),
        (1, 'unidade(s)'),
        (2, 'metro(s)'),
        (3, 'quilo(s)'),
        (4, 'jogo(s)'),
    ]
    codigo = models.IntegerField(verbose_name='Código', null=False, blank=False, unique=True)
    material = models.CharField(max_length=255, verbose_name='Nome')
    descricao = models.TextField(verbose_name='Descrição', max_length=500, null=True, blank=True)
    data = models.DateTimeField(auto_now=True, verbose_name='Data de cadastro')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='materiais_cadastrados', default=None)
    tipo = models.IntegerField(choices=TIPOS, default=1)

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None
    quantidade = None

    def __str__(self):

        return '%s | %s | Estoque: %d' % (self.codigo, self.material, self.quantidade.quantidade)


class MaterialQuantidade(models.Model):
    """
    Model que gerencia a tabela de controle da quantidade de materiais em estoque
    """
    material = models.OneToOneField(Material, on_delete=models.CASCADE, related_name='quantidade')
    quantidade = models.IntegerField(verbose_name='Quantidade', null=False, blank=False)

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class Ordem(models.Model):
    """
    Model que gerencia a tabela de controle de ordens de entrada e saída do almoxarifado.
    Tem o intuito de documentar as entradas e saídas de materiais
    """
    TIPO = [
        (0, 'Entrada'),
        (1, 'Saida'),
    ]

    data = models.DateTimeField(auto_now=True, verbose_name='Data de cadastro')
    tipo = models.IntegerField(choices=TIPO, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='almoxaridado_ordens')

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None
    id = None

    def __str__(self):

        return '%s | %s' % (self.id, self.data)


class MaterialEntrada(models.Model):
    """
    Model que gerencia a tabela de entradas de materiais no almoxarifado
    """
    material = models.ForeignKey(Material, on_delete=models.PROTECT, related_name='entradas')
    quantidade = models.IntegerField(verbose_name='Quantidade', null=True, blank=True)
    data = models.DateTimeField(auto_now=True, verbose_name='Data de entrada')
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT, related_name='aquisicoes')
    observacao = models.TextField(verbose_name='Observação', max_length=500, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='almoxarifado_entradas', default=None)
    ordem = models.ForeignKey(Ordem, on_delete=models.CASCADE, related_name='almoxarifado_ordem_entrada', default=None)

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class MaterialSaida(models.Model):
    """
    Model qeu gerencia a tabela de saídas de materiais do almoxarifado
    """
    material = models.ForeignKey(Material, on_delete=models.PROTECT, related_name='saidas')
    quantidade = models.IntegerField(verbose_name='Quantidade', null=True, blank=True)
    data = models.DateTimeField(auto_now=True, verbose_name='Data de saída')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='almoxarifado_saidas')
    user_to = models.ForeignKey(User, on_delete=models.PROTECT, related_name='almoxarifado_retiradas')
    observacao = models.TextField(verbose_name='Observação', max_length=500, null=True, blank=True)
    ordem = models.ForeignKey(Ordem, on_delete=models.CASCADE, related_name='almoxarifado_ordem_saida', default=None)

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None
