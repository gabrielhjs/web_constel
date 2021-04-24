import csv
from io import StringIO
from datetime import date
from typing import List, Dict

from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import IntegrityError
from django.contrib import messages
from django.db.models import Q, QuerySet
from django.http import HttpRequest

from .models import Cartao, Upload


def handle_csv_file(file: InMemoryUploadedFile, form_data: Dict, request: HttpRequest) -> List:
  data_list = []

  with StringIO(file.read().decode("latin-1")) as csv_file:
    data = csv.reader(csv_file, delimiter=";")
    next(data)

    try:
      upload = Upload(
        user=request.user,
        file_name=form_data.get("file_csv"),
        data_referencia=form_data.get("data")
      )
      upload.save()

    except IntegrityError:
      messages.error(request, "A data referenciada já possui registros")

    else:
      for row in data:
        if (
          row[0]
          and row[3]
          and row[4]
          and row[6]
          and row[11]
        ):
          name = row[4].split(" ", maxsplit=1)

          user_to, created = User.objects.get_or_create(
            username=row[3],
            defaults={"first_name": name[0], "last_name": name[1]}
          )

          if created:
            user_to.save()

          Cartao(
            user_to=user_to,
            user_to_name=row[4],
            user_to_cpf=row[0],
            user_to_birthday=date(day=int(row[6][:2]), month=int(row[6][2:4]), year=int(row[6][4:6])),
            value=float(row[11]) if row[11] else 0,
            upload=upload
          ).save()


def get_uploads(query: Q = Q()) -> QuerySet:

  return Upload.objects.filter(query).values(
    "id",
    "user__first_name",
    "user__last_name",
    "file_name",
    "data",
    "data_referencia",
  ).order_by(
    "data",
  )


def get_upload_data(query: Q = Q()) -> QuerySet:

  return Cartao.objects.filter(query).values(
    "user_to__username",
    "user_to__first_name",
    "user_to__last_name",
    "upload__id",
    "value",
  ).order_by(
    "user_to__first_name",
    "user_to__last_name",
  )
