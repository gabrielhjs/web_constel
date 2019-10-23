from django.urls import path, include

from . import views

urlpatterns = [
    path('', include('apps.web_gc.urls')),
    path('', views.index, name='index'),
]
