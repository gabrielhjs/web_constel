from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Km(models.Model):
  objects: models.manager.Manager

  km_initial = models.FloatField(null=True, blank=True)
  km_final = models.FloatField(null=True, blank=True)
  user = models.ForeignKey(User, on_delete=models.PROTECT, null=False, related_name="%(class)s_users+")
  user_to = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="%s(class)s_users_to+")
  date = models.DateField(default=timezone.now)
  status = models.BooleanField(default=True)
