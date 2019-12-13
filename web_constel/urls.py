from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('apps.almoxarifado.urls')),
    path('', include('apps.patrimonio.urls')),
    path('', include('constel.urls')),
    path('admin/', admin.site.urls),
]
