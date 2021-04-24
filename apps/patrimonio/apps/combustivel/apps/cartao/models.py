from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class Upload(models.Model):
  objects = models.manager.Manager

  user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user_cartao_uploads")
  file_name = models.CharField(max_length=255, null=False)
  data = models.DateTimeField(auto_now_add=True)
  data_referencia = models.DateField(null=False, unique=True)


class Cartao(models.Model):
  objects = models.manager.Manager

  class Meta:
    unique_together = ["user_to", "upload"]

  value_validators = (
    MinValueValidator(0.0, "O valor mínimo deve ser maior ou igual a R$ 0,00"),
  )

  user_to = models.ForeignKey(User, on_delete=models.PROTECT, related_name="cartao_recepcoes")
  user_to_name = models.CharField(max_length=255)
  user_to_cpf = models.CharField(max_length=11, null=False)
  user_to_birthday = models.DateField()
  value = models.FloatField(null=False, blank=False, validators=value_validators)
  upload = models.ForeignKey(Upload, on_delete=models.CASCADE, related_name="cartao_uploads")
