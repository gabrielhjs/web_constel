from django.contrib.auth.models import User
from django.db import models


class Ordem(models.Model):
  """
  Model que gerencia a tabela de controle de ordens de entrada e saída do patrimonio.
  Tem o intuito de documentar as entradas e saídas de materiais
  """
  TIPO = [
    (0, 'Entrada'),
    (1, 'Saida'),
  ]
  data = models.DateTimeField(auto_now=True, verbose_name='Data de cadastro')
  tipo = models.IntegerField(choices=TIPO, null=False, blank=False)
  user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='patrimonio_ordens')

  # Default fields (apenas para não gerar alertas na IDE)
  objects = None
  id = None

  def __str__(self):
    return '%s | %s' % (self.id, self.data)
