from django.contrib import admin
from .models import *


admin.site.register(Fornecedor)
admin.site.register(Material)
admin.site.register(MaterialQuantidade)
admin.site.register(Ordem)
admin.site.register(MaterialEntrada)
admin.site.register(MaterialSaida)
