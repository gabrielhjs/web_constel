from django.contrib import admin

from .models import *


class AdimOnt(admin.ModelAdmin):
    search_fields = ('codigo', 'status', 'secao__nome', 'modelo__nome', )
    list_display = ('codigo', 'status', 'secao', 'modelo', )
    list_filter = ('status', 'secao', 'modelo', )


class AdminOntEntrada(admin.ModelAdmin):
    search_fields = ('data', 'ont__codigo', 'user__username', 'user__first_name', 'user__las_name', )
    list_display = ('data', 'ont', 'user', )


admin.site.register(Ont, AdimOnt)
admin.site.register(OntEntrada)
admin.site.register(OntSaida)
admin.site.register(OntAplicado)
admin.site.register(Secao)
admin.site.register(Modelo)
admin.site.register(Cliente)
