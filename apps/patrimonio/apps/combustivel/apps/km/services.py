import datetime
from datetime import date

from django.contrib.auth.models import User
from django.db.models import QuerySet, Subquery, OuterRef, F, Q, Count, ExpressionWrapper, FloatField, Sum
from django.db.models.functions import Coalesce

from constel.models import GestorUser
from .models import Km
from ..cartao.models import Cartao
from ..talao.models import EntregaVale


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


def query_today_pending(query: Q = Q()) -> QuerySet:
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


def query_general_report(initial_date: str, final_date: str, owner: str) -> QuerySet:

  query = Q()
  query_cartao = Q()
  query_vales = Q()

  if owner:
    query = query & Q(
      Q(user_to__username__icontains=owner) |
      Q(user_to__first_name__icontains=owner) |
      Q(user_to__last_name__icontains=owner))

    query_cartao = query_cartao & Q(
      Q(user_to__username__icontains=owner) |
      Q(user_to__first_name__icontains=owner) |
      Q(user_to__last_name__icontains=owner))

    query_vales = query_vales & Q(
      Q(user_to__username__icontains=owner) |
      Q(user_to__first_name__icontains=owner) |
      Q(user_to__last_name__icontains=owner))

  if initial_date:
    data_inicial = datetime.datetime.strptime(initial_date, "%Y-%m-%d").date()
    query = query & Q(date__gte=data_inicial)
    query_cartao = query_cartao & Q(upload__data_referencia__gte=data_inicial)
    query_vales = query_vales & Q(data__gte=data_inicial)

  if final_date:
    data_final = datetime.datetime.strptime(final_date, "%Y-%m-%d").date()
    query = query & Q(date__lte=data_final)
    query_cartao = query_cartao & Q(upload__data_referencia__lte=data_final)
    query_vales = query_vales & Q(data__lte=data_final)

  vales = EntregaVale.objects.filter(
    query_vales,
    user_to=OuterRef("user_to")
  ).values(
    "user_to"
  ).annotate(
    total=Sum(F("valor"))
  ).values(
    "total"
  )

  cartao = Cartao.objects.filter(
    query_cartao,
    user_to=OuterRef("user_to")
  ).values(
    "user_to"
  ).annotate(
    total=Sum(F("value"))
  ).values(
    "total"
  )

  km = Km.objects.filter(query).annotate(
    distancia=ExpressionWrapper(F("km_final") - F("km_initial"), FloatField())
  ).values(
    "user_to"
  ).annotate(
    total_distancia=Sum(F("distancia")),
    total_vale=Coalesce(Subquery(vales, FloatField()), 0),
    total_cartao=Coalesce(Subquery(cartao, FloatField()), 0),
  ).annotate(
    indice=ExpressionWrapper(F("total_distancia")/(F("total_vale") + F("total_cartao")), FloatField()),
    total=ExpressionWrapper(F("total_vale") + F("total_cartao"), FloatField()),
  ).values(
    "user__first_name",
    "user__last_name",
    "user_to__first_name",
    "user_to__last_name",
    "total_distancia",
    "total_vale",
    "total_cartao",
    "total",
    "km_final",
    "indice"
  ).exclude(
    total_distancia__isnull=True
  ).exclude(
    total__isnull=True
  ).order_by(
    "-indice"
  )

  return km
