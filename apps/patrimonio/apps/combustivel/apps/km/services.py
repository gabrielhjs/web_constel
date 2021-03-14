from datetime import date

from django.contrib.auth.models import User
from django.db.models import QuerySet, Subquery, OuterRef, F, Q

from constel.models import GestorUser
from .models import Km


def get_user_team(query: Q = Q()) -> QuerySet:
  return GestorUser.objects.filter(query)


def get_user_team_initial_km(query: Q = Q()) -> QuerySet:
  registred_team = Km.objects.filter(date__gte=date.today()).values("user_to__id")
  return get_user_team(query).exclude(user__id__in=registred_team)


def set_user_team_initial_km(user_id: int, gestor_id: int, km: int) -> None:

  Km.objects.create(
    km_initial=km,
    user=User.objects.get(id=gestor_id),
    user_to=User.objects.get(id=user_id),
  ).save()


def get_user_team_final_km(user_id: int) -> QuerySet:
  return Km.objects.filter(user__id=user_id, date__gte=date.today(), km_final__isnull=True)


def is_team(user_id: int, gestor_id: int) -> bool:

  if GestorUser.objects.filter(user__id=user_id, gestor_id=gestor_id).exists():
    return True

  return False


def query_km_team(query: Q = Q()) -> QuerySet:

  km = Km.objects.filter(query).values(
    "km_initial",
    "km_final",
    "date",
    "user_to__first_name",
    "user_to__last_name",
    "user_to__username",
  ).order_by(
    "-date",
    "user_to__first_name",
    "user_to__last_name",
  )

  return km
