from django.contrib import admin

from .models import UserType, Veiculo


class AdminVeiculo(admin.ModelAdmin):
    search_fields = ('modelo', 'placa', 'user__username', 'user__first_name',)
    list_display = ('user', 'modelo', 'placa', 'cor',)


class AdminUserType(admin.ModelAdmin):
    search_fields = ('user__username', 'user__first_name',)
    list_display = ('user', 'is_passive',)


admin.site.register(UserType, AdminUserType)
admin.site.register(Veiculo, AdminVeiculo)
