from django.contrib import admin

from .models import *

admin.site.register(Ferramenta)
admin.site.register(FerramentaQuantidade)
admin.site.register(FerramentaQuantidadeFuncionario)
admin.site.register(FerramentaEntrada)
admin.site.register(FerramentaSaida)
