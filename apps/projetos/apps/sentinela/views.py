from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def consulta_queue(request: HttpRequest) -> HttpResponse:
  return render(request, "sentinela/consulta_queue.html")
