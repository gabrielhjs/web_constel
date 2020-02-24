from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


class Talao(models.Model):
    """
    Classe de talões que contém vales
    """

    STATUS_CHOISES = [
        (0, 'Disponível'),
        (1, 'Em uso'),
        (2, 'Usado'),
    ]

    HELP_TEXT = 'Insira um valor válido de talão'

    talao = models.IntegerField(
        unique=True,
        validators=[
            MinValueValidator(1, 'Talão inválido'),
            MaxValueValidator(999999, 'Talão inválido'),
        ],
        verbose_name='Talao',
        help_text=HELP_TEXT,
    )
    status = models.IntegerField(choices=STATUS_CHOISES, default=0)

    def __str__(self):
        return '%s' % self.talao

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class Vale(models.Model):
    """
    Classe de vales que podem ser distribuidos para os funcionarios
    """

    STATUS_CHOISES = [
        (0, 'Indisponível'),
        (1, 'Disponível'),
        (2, 'Usado'),
    ]

    vale = models.IntegerField(
        unique=True,
        validators=[
            MinValueValidator(10000, 'Vale inválido'),
            MaxValueValidator(9999999, 'Vale inválido'),
        ],
    )
    status = models.IntegerField(choices=STATUS_CHOISES, default=0)
    talao = models.ForeignKey(Talao, on_delete=models.CASCADE, related_name='talao_vales')

    def __str__(self):
        return '%s' % self.vale

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class Combustivel(models.Model):
    """
    Classe que contém os caombustíveis que podem ser utilizados nos vales
    """

    HELP_TEXT = 'Insira um combustível'
    combustivel = models.CharField(unique=True, max_length=30, help_text=HELP_TEXT, error_messages={
        'unique': 'Este combustível já está cadastrado no sistema!',
    })

    def __str__(self):
        return '%s' % self.combustivel

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None


class Posto(models.Model):
    posto = models.CharField(max_length=100, verbose_name='Posto')
    rua = models.CharField(max_length=255)
    numero = models.IntegerField(null=False, verbose_name='N°')
    cidade = models.CharField(max_length=255, default='Curitiba')
    estado = models.CharField(max_length=255, default='Paraná')
    pais = models.CharField(max_length=255, default='Brasil')

    def __str__(self):
        return '%s' % self.posto

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None
    DoesNotExist = None


class CadastroTalao(models.Model):
    """
    Classe que registra o cadastro de talões no sistema
    """

    talao = models.ForeignKey(Talao, on_delete=models.CASCADE, related_name='talao_cadastro')
    data = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, default=None, on_delete=models.PROTECT)

    def __str__(self):
        return '%s - %.19s' % (self.talao, self.data)

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None
    DoesNotExist = None


class EntregaTalao(models.Model):
    """
    Classe que registra a entrega dos talões para os encarregados
    """

    talao = models.ForeignKey(Talao, on_delete=models.CASCADE, related_name='talao_entrega')
    data = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, default=None, on_delete=models.PROTECT, related_name='talao_user')
    user_to = models.ForeignKey(
        User, default=None,
        on_delete=models.PROTECT,
        related_name='talao_user_to',
        verbose_name='Para',
        help_text='Usuário que irá receber o talão'
    )

    def __str__(self):
        return '%s - %.19s' % (self.talao, self.data)

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None
    DoesNotExist = None


class EntregaVale(models.Model):
    """
    Classe que registra a entrega de vales para os funcionários
    """

    vale = models.ForeignKey(Vale, on_delete=models.CASCADE, related_name='vale_entrega')
    data = models.DateTimeField(auto_now=True)
    combustivel = models.ForeignKey(Combustivel, on_delete=models.PROTECT, verbose_name='Combustível')
    valor = models.FloatField(null=True)
    observacao = models.TextField('Observações', blank=True, max_length=255)
    user = models.ForeignKey(User, default=None, on_delete=models.PROTECT, related_name='vale_user')
    user_to = models.ForeignKey(
        User, default=None,
        on_delete=models.PROTECT,
        related_name='vale_user_to',
        verbose_name='Para',
        help_text='Usuário que irá receber o vale combustível'
    )
    posto = models.ForeignKey(
        Posto,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        default=None,
        related_name='vale_posto',
    )

    def __str__(self):
        return '%s - %.19s' % (self.vale, self.data)

    def valor_moeda(self):
        return 'R$ {:8.2f}'.format(self.valor)

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None