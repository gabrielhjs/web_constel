from django.contrib.auth.models import User
from django.db import models


class Km(models.Model):
  objects: models.manager.Manager

  km_initial = models.FloatField(null=False)
  km_final = models.FloatField(null=True)
  user = models.ForeignKey(User, on_delete=models.PROTECT, null=False, related_name="%(class)s_users+")
  user_to = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="%s(class)s_users_to+")
  date = models.DateField(auto_now_add=True)
