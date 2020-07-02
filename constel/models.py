from django.db import models
from django.contrib.auth.models import User


class UserType(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_type')
    is_passive = models.BooleanField(default=True)

    def __str__(self):
        return self.user.get_full_name()


class Veiculo(models.Model):
    """
    Classe que contém os veículos do funcionários
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='veiculos', verbose_name='Usuário')
    modelo = models.CharField(max_length=30)
    placa = models.CharField(max_length=8)
    cor = models.CharField(max_length=100)

    # Default fields (apenas para não gerar alertas na IDE)
    objects = None
    DoesNotExist = None
