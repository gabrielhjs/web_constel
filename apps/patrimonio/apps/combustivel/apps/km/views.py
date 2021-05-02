import datetime

from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from constel.forms import FormFiltraQ, FormDataInicialFinalFuncionario
from constel.apps.controle_acessos.decorator import permission
from . import menu as mn, services, forms


@login_required()
def view_menu_principal(request: HttpRequest) -> HttpResponse:
  context = mn.principal(request)
  
  return render(request, "constel/v2/app.html", context)


def view_menu_registros(request: HttpRequest) -> HttpResponse:
  context = mn.registros(request)

  return render(request, "constel/v2/app.html", context)


def view_menu_consultas(request: HttpRequest) -> HttpResponse:
  context = mn.consultas(request)

  return render(request, "constel/v2/app.html", context)


@login_required()
@permission("patrimonio - combustivel - km")
def view_consulta_km_time(request: HttpRequest) -> HttpResponse:
  menu = mn.consultas(request)

  q = request.GET.get("q", "")

  form = FormFiltraQ(
    "nome ou matrícula",
    initial={
      "q": q,
    }
  )

  query = Q(user__id=request.user.id)

  if q != "":
    query = query & Q(
      Q(user_to__first_name__icontains=q) |
      Q(user_to__last_name__icontains=q) |
      Q(user_to__username__icontains=q)
    )

  itens = services.query_km_team(query)

  paginator = Paginator(itens, 50)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)

  context = {
    "page_obj": page_obj,
    "form": form,
    "form_submit_text": "Filtrar"
  }
  context.update(menu)

  return render(request, "km/consultar_km_time.html", context)


@login_required()
@permission("patrimonio - combustivel - km", "patrimonio")
def view_consulta_km_hoje(request: HttpRequest) -> HttpResponse:
  menu = mn.consultas(request)

  q = request.GET.get("q", "")

  form = FormFiltraQ(
    "nome ou matrícula",
    initial={
      "q": q,
    }
  )

  query = Q()

  if q != "":
    query = query & Q(
      Q(user_to__first_name__icontains=q) |
      Q(user_to__last_name__icontains=q) |
      Q(user_to__username__icontains=q) |
      Q(user__first_name__icontains=q) |
      Q(user__last_name__icontains=q) |
      Q(user__username__icontains=q)
    )

  itens = services.query_km(query)

  paginator = Paginator(itens, 50)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)

  context = {
    "page_obj": page_obj,
    "form": form,
    "form_submit_text": "Filtrar"
  }
  context.update(menu)

  return render(request, "km/consultar_km_hoje.html", context)


@login_required()
@permission("patrimonio - combustivel - km", "patrimonio")
def view_consulta_km_pendencias_hoje(request: HttpRequest) -> HttpResponse:
  menu = mn.consultas(request)

  q = request.GET.get("q", "")

  form = FormFiltraQ(
    "nome ou matrícula",
    initial={
      "q": q,
    }
  )

  query = Q()

  if q != "":
    query = query & Q(
      Q(gestor__first_name__icontains=q) |
      Q(gestor__last_name__icontains=q) |
      Q(gestor__username__icontains=q)
    )

  itens = services.query_today_pending(query)

  paginator = Paginator(itens, 50)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)

  context = {
    "page_obj": page_obj,
    "form": form,
    "form_submit_text": "Filtrar"
  }
  context.update(menu)

  return render(request, "km/consultar_pendencias_hoje.html", context)


def view_menu_relatorios(request: HttpRequest) -> HttpResponse:
  context = mn.relatorios(request)

  return render(request, "constel/v2/app.html", context)


def view_relatorio_geral(request: HttpRequest) -> HttpResponse:
  menu = mn.relatorios(request)

  funcionario = request.GET.get("funcionario", "")
  data_inicial = request.GET.get("data_inicial", "")
  data_final = request.GET.get("data_final", "")

  form = FormDataInicialFinalFuncionario(initial={
    "funcionario": funcionario,
    "data_inicial": data_inicial,
    "data_final": data_final
  })

  itens = services.query_general_report(data_inicial, data_final, funcionario)

  context = {
    "itens": itens,
    "form": form,
    "form_submit_text": "Filtrar"
  }
  context.update(menu)

  return render(request, "km/relatorio_geral.html", context)


@login_required()
@permission("patrimonio - combustivel - km")
def view_registrar_km_inicial(request: HttpRequest) -> HttpResponse:
  menu = mn.registros(request)

  q = request.GET.get("q", "")

  form = FormFiltraQ(
    "nome ou matrícula",
    initial={
      "q": q,
    }
  )

  query = Q(gestor__id=request.user.id)

  if q != "":
    query = query & Q(
      Q(user__first_name__icontains=q) |
      Q(user__last_name__icontains=q) |
      Q(user__username__icontains=q)
    )

  itens = services.get_user_team_initial_km(query).values(
    "user__id",
    "user__username",
    "user__first_name",
    "user__last_name",
  )

  paginator = Paginator(itens, 50)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)

  context = {
    "page_obj": page_obj,
    "form": form,
    "form_submit_text": "Filtrar",
    "details": "patrimonio_combustivel_km_registros_inicial"
  }
  context.update(menu)

  return render(request, "km/registrar_km_inicial.html", context)


@login_required()
@permission("patrimonio - combustivel - km")
def view_registrar_km_final(request: HttpRequest) -> HttpResponse:
  menu = mn.registros(request)

  q = request.GET.get("q", "")

  form = FormFiltraQ(
    "nome ou matrícula",
    initial={
      "q": q,
    }
  )

  query = Q()

  if q != "":
    query = query & Q(
      Q(user_to__first_name__icontains=q) |
      Q(user_to__last_name__icontains=q) |
      Q(user_to__username__icontains=q)
    )

  itens = services.get_user_team_final_km(query).values(
    "id",
    "date",
    "user_to__id",
    "user_to__username",
    "user_to__first_name",
    "user_to__last_name",
  ).order_by(
    "user_to__first_name",
    "user_to__last_name",
    "date",
  )

  paginator = Paginator(itens, 50)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)

  context = {
    "page_obj": page_obj,
    "form": form,
    "form_submit_text": "Filtrar",
    "details": "patrimonio_combustivel_km_registros_final"
  }
  context.update(menu)

  return render(request, "km/registrar_km_final.html", context)


@login_required()
@permission("patrimonio - combustivel - km")
def view_registrar_km_inicial_detalhes(request: HttpRequest, user_id: int) -> HttpResponse:
  menu = mn.registros(request)

  form = forms.KmForm(user_id=user_id, gestor_id=request.user.id, data=request.POST or None)

  if request.method == "POST":
    if form.is_valid():
      km = form.cleaned_data["km"]
      services.set_user_team_initial_km(user_id, request.user.id, km)

      return HttpResponseRedirect("/patrimonio/combustivel/km/registros/inicial")

  context = {
    "form": form,
    "form_submit_text": "Registrar"
  }
  context.update(menu)

  return render(request, "km/registrar_km_form.html", context)


@login_required()
@permission("patrimonio - combustivel - km")
def view_registrar_km_final_detalhes(request: HttpRequest, user_id: int, km_id: int) -> HttpResponse:
  menu = mn.registros(request)

  form = forms.KmForm(km_id=km_id, gestor_id=request.user.id, user_id=user_id, data=request.POST or None)

  if request.method == "POST":
    if form.is_valid():
      km = form.cleaned_data["km"]
      services.set_user_team_final_km(km_id, km)

      return HttpResponseRedirect("/patrimonio/combustivel/km/registros/final")

  context = {
    "form": form,
    "form_submit_text": "Registrar"
  }
  context.update(menu)

  return render(request, "km/registrar_km_form.html", context)
