from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render

from apps.patrimonio.apps.combustivel.apps.talao.menu import menu_consultas
from constel.apps.controle_acessos.decorator import permission
from constel.forms import FormDataInicialFinal, FormFiltraQ

from .menu import menu_principal
from .forms import FormUploadCSV
from .import services


@login_required()
def index(request: HttpRequest) -> HttpResponse:
  context = menu_principal(request)

  return render(request, "constel/v2/app.html", context)


@login_required()
@permission('patrimonio - combustivel - km',)
def importa_csv(request: HttpRequest) -> HttpResponse:
  menu = menu_principal(request)

  form = FormUploadCSV(data=request.POST or None, files=request.FILES or None)

  if request.method == "POST":
    if form.is_valid():
      services.handle_csv_file(request.FILES.get("file_csv"), form.cleaned_data, request)

      return HttpResponseRedirect("/patrimonio/combustivel/cartao/importar")

  context = {
    "form": form,
    "form_submit_text": "Importar dados"
  }
  context.update(menu)

  return render(request, "cartao/importar_dados.html", context)


@login_required()
@permission('patrimonio - combustivel - km',)
def consulta_depositos(request: HttpRequest) -> HttpResponse:
  menu = menu_consultas(request)

  data_inicial = request.GET.get("data_inicial", "")
  data_final = request.GET.get("data_final", "")

  form = FormDataInicialFinal(
    initial={
      "data_inicial": data_inicial,
      "data_final": data_final
    },
  )

  query = Q()

  if data_inicial:
    data_inicial = datetime.strptime(data_inicial, "%Y-%m-%d").date()
    query = query & Q(data_referencia__gte=data_inicial)

  if data_final:
    data_final = datetime.strptime(data_final, "%Y-%m-%d").date()
    query = query & Q(data_referencia__lte=data_final)

  itens = services.get_uploads(query)

  paginator = Paginator(itens, 50)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)

  context = {
    "page_obj": page_obj,
    "form": form,
    "form_submit_text": 'Filtrar'
  }
  context.update(menu)

  return render(request, "cartao/consultar_uploads.html", context)


@login_required()
@permission('patrimonio - combustivel - km',)
def consulta_depositos_detalhe(request: HttpRequest, upload: int) -> HttpResponse:
  menu = menu_consultas(request)

  q = request.GET.get("q", "")

  form = FormFiltraQ(
    initial={
      "q": q
    },
    descricao="nome ou matrícula"
  )

  query = Q(upload__id=upload)

  if q:
    query = Q(query & Q(
      Q(user_to__username__icontains=q) |
      Q(user_to__first_name__icontains=q) |
      Q(user_to__last_name__icontains=q)
    ))

  itens = services.get_upload_data(query)

  paginator = Paginator(itens, 50)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)

  context = {
    "page_obj": page_obj,
    "form": form,
    "form_submit_text": 'Filtrar'
  }
  context.update(menu)

  return render(request, "cartao/consultar_uploads_detalhe.html", context)
