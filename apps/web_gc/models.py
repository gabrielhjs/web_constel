from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Talao(models.Model):
    """Classe de talões que contém vales"""

    STATUS_CHOISES = [
        (0, 'Disponível para uso'),
        (1, 'Em uso'),
        (2, 'Usado'),
    ]

    talao = models.IntegerField(
        unique=True,
        validators=[
            MinValueValidator(100, 'Talão inválido'),
            MaxValueValidator(999999, 'Talão inválido'),
        ],
    )
    status = models.IntegerField(choices=STATUS_CHOISES, default=0, editable=True)
    data = models.DateTimeField(auto_now=True, editable=True)

    def __str__(self):
        return '%s' % self.talao


class Vale(models.Model):
    """Classe de vales que podem ser distribuidos para os funcionarios"""

    STATUS_CHOISES = [
        (0, 'Indisponível para uso'),
        (1, 'Disponível'),
        (2, 'Usado'),
    ]

    vale = models.IntegerField(
        unique=True,
        validators=[
            MinValueValidator(10000, 'Vale inválido'),
            MaxValueValidator(999999, 'Vale inválido'),
        ],
    )
    status = models.IntegerField(choices=STATUS_CHOISES, default=0)
    talao = models.ForeignKey(Talao, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % self.vale


class Combustivel(models.Model):
    """Classe que contém os caombustíveis que podem ser utilizados nos vales"""

    HELP_TEXT = 'Insira um combustível'

    combustivel = models.CharField(unique=True, max_length=10, help_text=HELP_TEXT)

    def __str__(self):
        return '%s' % self.combustivel


class CadastroTalao(models.Model):
    """Classe que registra o cadastro de talões no sistema"""

    talao = models.ForeignKey(Talao, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % self.talao


class EntregaTalao(models.Model):
    """Classe que registra a entrega dos talões para os encarregados"""

    HELP_TEXT_TALAO = 'Insira um talão cadastrado no sistema'

    talao = models.ForeignKey(Talao, on_delete=models.CASCADE, help_text=HELP_TEXT_TALAO)
    data = models.DateTimeField(auto_now=True)


class EntregaVale(models.Model):
    """Classe que registra a entrega de vales para os funcionários"""

    vale = models.ForeignKey(Vale, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now=True)
    combustivel = models.ForeignKey(Combustivel, on_delete=models.PROTECT, verbose_name='Combustível')
    valor = models.FloatField(null=True)
    observacao = models.TextField('Observações', blank=True, max_length=255)
