from datetime import date

from django.contrib.auth.models import User
from django.db.models import QuerySet, Subquery, OuterRef, F, Q, Count

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


def get_user_team_final_km(query: Q = Q()) -> QuerySet:
  return Km.objects.filter(query, date__gte=date.today(), km_final__isnull=True)


def set_user_team_final_km(user_id: int, gestor_id: int, km_final: float) -> None:

  km = Km.objects.get(
    date__gte=date.today(),
    km_final__isnull=True,
    user=User.objects.get(id=gestor_id),
    user_to=User.objects.get(id=user_id),
  )

  km.km_final = km_final

  km.save()


def is_team(user_id: int, gestor_id: int) -> bool:

  if GestorUser.objects.filter(user__id=user_id, gestor_id=gestor_id).exists():
    return True

  return False


def is_final_gte_initial(user_id: int, gestor_id: int, km_final: float) -> (bool, int):
  if Km.objects.filter(
    date__gte=date.today(),
    km_final__isnull=True,
    user=User.objects.get(id=gestor_id),
    user_to=User.objects.get(id=user_id),
  ).exists():
    km_initial = Km.objects.get(
      date__gte=date.today(),
      km_final__isnull=True,
      user=User.objects.get(id=gestor_id),
      user_to=User.objects.get(id=user_id),
    ).km_initial

    if km_initial > km_final:
      return False, km_initial

  return True, 0


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


def query_km(query: Q = Q()) -> QuerySet:

  km = Km.objects.filter(query, date__gte=date.today()).values(
    "km_initial",
    "km_final",
    "date",
    "user__first_name",
    "user__last_name",
    "user_to__first_name",
    "user_to__last_name",
  ).order_by(
    "-date",
    "user__first_name",
    "user__last_name",
    "user_to__first_name",
    "user_to__last_name",
  )

  return km


def query_today_pending(user_id: int, query: Q = Q()) -> QuerySet:
  registred_initial = Km.objects.filter(
    user__id=OuterRef("gestor__id"),
    date__gte=date.today()
  ).values(
    "user__id"
  ).annotate(
    total=Count(F("user_to__id"))
  ).values("total")

  registred_final = Km.objects.filter(
    user__id=OuterRef("gestor__id"),
    date__gte=date.today(),
    km_final__isnull=False
  ).values(
    "user__id"
  ).annotate(
    total=Count(F("user_to__id"))
  ).values("total")

  # print(list(registred_initial))
  # print(list(registred_final))

  pendency = get_user_team(query).values(
    "gestor__first_name",
    "gestor__last_name",
  ).annotate(
    total=Count(F("user__id")),
    initial=Count(F("user__id")) - Subquery(registred_initial),
    final=Count(F("user__id")) - Subquery(registred_final),
  )

  return pendency.values(
    "gestor__username",
    "gestor__first_name",
    "gestor__last_name",
    "total",
    "initial",
    "final",
  )

