from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.response import Response

from .serializers import SerializerWfmContratos, SerializerWfmNovoContrato
from .models import SentinelaContratos


def consulta_queue(request: HttpRequest) -> HttpResponse:

  page_obj = SentinelaContratos.objects.all().order_by("-id").values(
    "contrato",
    "recurso",
    "sinal_ont",
    "sinal_olt",
    "created_at",
    "status_sentinela",
    "tipo",
  )

  context = {
    "page_obj": page_obj,
    "sentinela_url": settings.SENTINELA_WE
  }

  return render(request, "sentinela/consulta_queue.html", context)


class ViewConsultaNovosContratos(APIView):
  renderer_classes = [JSONRenderer]

  @staticmethod
  def post(request):
    serializer = SerializerWfmContratos(data=request.data)

    response = {}

    if serializer.is_valid(raise_exception=True):
      atividade_existe = serializer.save()
      status_code = status.HTTP_201_CREATED

      response.update({
        "atividade_existe": atividade_existe,
      })

    else:
      status_code = status.HTTP_400_BAD_REQUEST

    response.update({"status_code": status_code})

    return Response(response, status=status_code)


class ViewInsereNovoContrato(APIView):
  renderer_classes = [JSONRenderer]

  @staticmethod
  def post(request):
    serializer = SerializerWfmNovoContrato(data=request.data)

    response = {}

    if serializer.is_valid(raise_exception=True):
      atividade_criada = serializer.save()
      status_code = status.HTTP_201_CREATED

      response.update({
        "atividade_existe": atividade_criada,
      })

    else:
      status_code = status.HTTP_400_BAD_REQUEST

    response.update({"status_code": status_code})

    return Response(response, status=status_code)
