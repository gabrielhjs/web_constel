from django.db import models
from django.contrib.auth.models import User


class Lista(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='lista_saida')
    user_to = models.ForeignKey(User, on_delete=models.PROTECT, related_name='lista_retirada')
    data = models.DateTimeField(auto_now=True, verbose_name='Lista criada em')

