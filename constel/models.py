from django.db import models
from django.contrib.auth.models import User


class UserType(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_passive = models.BooleanField(default=True)

    def __str__(self):
        return self.user.get_full_name()
