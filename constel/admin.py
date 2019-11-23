from django.contrib import admin

from .models import UserType, Veiculo


class AdminVeiculo(admin.ModelAdmin):
    list_filter = ('user__first_name', )
    list_display = ('user', 'modelo', 'placa', 'cor',)


admin.site.register(UserType)
admin.site.register(Veiculo, AdminVeiculo)
