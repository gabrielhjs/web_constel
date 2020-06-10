from django.contrib import admin

from .models import *


class AdimOnt(admin.ModelAdmin):
    search_fields = ('codigo', 'status', 'secao__nome', 'modelo__nome', )
    list_display = ('codigo', 'status', 'secao', 'modelo', )
    list_filter = ('status', 'secao', 'modelo', )


class AdminOntEntrada(admin.ModelAdmin):
    search_fields = ('data', 'ont__codigo')
    list_display = ('data', 'ont', 'user')


class AdminOntSaida(admin.ModelAdmin):
    search_fields = ('data', 'ont__codigo')
    list_display = ('data', 'ont', 'user_to')


admin.site.register(Ont, AdimOnt)
admin.site.register(OntEntrada, AdminOntEntrada)
admin.site.register(OntSaida, AdminOntSaida)
admin.site.register(OntAplicado)
admin.site.register(Secao)
admin.site.register(Modelo)
admin.site.register(Cliente)
