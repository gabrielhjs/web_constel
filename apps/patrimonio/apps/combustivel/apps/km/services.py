from datetime import date

from django.db.models import QuerySet

from constel.models import GestorUser
from .models import KmInicial


def get_user_team(user_id: int) -> QuerySet:
  return GestorUser.objects.filter(gestor__id=user_id)


def get_user_team_initial_km(user_id: int) -> QuerySet:
  registred_team = KmInicial.objects.filter(user__id=user_id, date__gte=date.today()).values("user__id")

  return get_user_team(user_id).exlude(user__id__in=registred_team)


def get_user_team_final_km(user_id: int) -> QuerySet:
  return KmInicial.objects.filter(user__id=user_id, date__gte=date.today())
