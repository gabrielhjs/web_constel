from django.db import models


class Talao(models.Model):
    STATUS_CHOISES = [
        (0, 'Disponível para uso'),
        (1, 'Em uso'),
        (2, 'Usado'),
    ]
    HELP_TEXT = "Insira um código válido de Talão"
    talao = models.IntegerField(unique=True, help_text=HELP_TEXT)
    status = models.IntegerField(choices=STATUS_CHOISES)


class Vale(models.Model):
    STATUS_CHOISES = [
        (0, 'Indisponível para uso'),
        (1, 'Disponível'),
        (2, 'Usado'),
    ]
    HELP_TEXT = "Insira um código válido de Vale"

    vale = models.IntegerField(unique=True, help_text=HELP_TEXT)
    status = models.IntegerField(choices=STATUS_CHOISES)
    talao = models.ForeignKey(Talao, on_delete=models.CASCADE)


class Combustivel(models.Model):
    HELP_TEXT = 'Insira um combustível'

    combustivel = models.CharField(max_length=10, help_text=HELP_TEXT)


class CadastroTalao(models.Model):
    talao = models.ForeignKey(Talao, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now=True)


class EntregaTalao(models.Model):
    HELP_TEXT_TALAO = 'Insira um talão cadastrado no sistema'

    talao = models.ForeignKey(Talao, on_delete=models.CASCADE, help_text=HELP_TEXT_TALAO)
    data = models.DateTimeField(auto_now=True)


class EntregaVale(models.Model):
    HELP_TEXT_VALE = 'Insira um vale cadastrado no sistema'
    HELP_TEXT_COMBUSTIVEL = 'Insira um combustível cadstrado no sistema'
    HELP_TEXT_VALOR = 'Insira o valor deste vale'

    vale = models.ForeignKey(Vale, on_delete=models.CASCADE, help_text=HELP_TEXT_VALE)
    data = models.DateTimeField(auto_now=True)
    combustivel = models.ForeignKey(Combustivel, on_delete=models.PROTECT, help_text=HELP_TEXT_COMBUSTIVEL)
    valor = models.FloatField(help_text=HELP_TEXT_VALOR)
    observacao = models.TextField('Observações', blank=True, max_length=255)
