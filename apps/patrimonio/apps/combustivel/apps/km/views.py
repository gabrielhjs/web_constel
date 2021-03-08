from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

import menu as mn
import services


def view_menu_principal(request: HttpRequest) -> HttpResponse:
  context = mn.principal(request)
  
  return render(request, "constel/v2/app.html", context)


def view_menu_registros(request: HttpRequest) -> HttpResponse:
  context = mn.registros(request)

  return render(request, "constel/v2/app.html", context)


def view_menu_consultas(request: HttpRequest) -> HttpResponse:
  context = mn.consultas(request)

  return render(request, "constel/v2/app.html", context)


def view_registrar_km_inicial(request: HttpRequest) -> HttpResponse:
  menu = mn.consultas(request)

  itens = services.get_user_team_initial_km(request.user.id)

  paginator = Paginator(itens, 50)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  context = {
    'page_obj': page_obj,
  }
  context.update(menu)

  return render(request, 'km/registrar_km_inicial.html', context)


def view_registrar_km_final(request: HttpRequest) -> HttpResponse:
  menu = mn.consultas(request)

  itens = services.get_user_team_final_km(request.user.id)

  paginator = Paginator(itens, 50)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  context = {
    'page_obj': page_obj,
  }
  context.update(menu)

  return render(request, 'km/registrar_km_final.html', context)
