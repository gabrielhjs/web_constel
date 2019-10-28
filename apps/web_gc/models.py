from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Talao(models.Model):
    """Classe de talões que contém vales"""

    STATUS_CHOISES = [
        (0, 'Disponível para uso'),
        (1, 'Em uso'),
        (2, 'Usado'),
    ]
    HELP_TEXT = "Insira um código válido de Talão"

    talao = models.IntegerField(
        unique=True,
        help_text=HELP_TEXT,
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
    HELP_TEXT = "Insira um código válido de Vale"

    vale = models.IntegerField(
        unique=True,
        help_text=HELP_TEXT,
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

    HELP_TEXT_VALE = 'Insira um vale cadastrado no sistema'
    HELP_TEXT_COMBUSTIVEL = 'Insira um combustível cadstrado no sistema'
    HELP_TEXT_VALOR = 'Insira o valor deste vale'

    vale = models.ForeignKey(Vale, on_delete=models.CASCADE, help_text=HELP_TEXT_VALE)
    data = models.DateTimeField(auto_now=True)
    combustivel = models.ForeignKey(Combustivel, on_delete=models.PROTECT, help_text=HELP_TEXT_COMBUSTIVEL)
    valor = models.FloatField(help_text=HELP_TEXT_VALOR)
    observacao = models.TextField('Observações', blank=True, max_length=255)
