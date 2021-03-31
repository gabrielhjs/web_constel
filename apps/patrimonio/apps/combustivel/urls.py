from django.urls import path, include


urlpatterns = [
    # Apps
    path('', include('apps.patrimonio.apps.combustivel.apps.talao.urls')),
    path('', include('apps.patrimonio.apps.combustivel.apps.km.urls')),
    path('', include('apps.patrimonio.apps.combustivel.apps.cartao.urls')),
]
