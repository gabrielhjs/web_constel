from django.test import SimpleTestCase
from django.urls import reverse, resolve

from apps.web_gc.views import *


class TestUrls(SimpleTestCase):

    def test_cadastro_talao_url_is_solved(self):
        url = reverse('cadastro_talao')
        self.assertEquals(resolve(url).func, view_cadastrar_talao)

    def test_cadastro_combustivel_url_is_solved(self):
        url = reverse('cadastro_combustivel')
        self.assertEquals(resolve(url).func, view_cadastrar_combustivel)

    def test_entrega_talao_url_is_solved(self):
        url = reverse('entrega_talao')
        self.assertEquals(resolve(url).func, view_entrega_talao)

    def test_entrega_vale_url_is_solved(self):
        url = reverse('entrega_vale')
        self.assertEquals(resolve(url).func, view_entrega_vale)

    def test_index_url_is_solved(self):
        url = reverse('gc_index')
        self.assertEquals(resolve(url).func, view_index)

    def test_consulta_talao_url_is_solved(self):
        url = reverse('consulta_talao')
        self.assertEquals(resolve(url).func, view_taloes)

    def test_detalhes_talao_url_is_solved(self):
        url = reverse('detalhes_talao', kwargs={'talao_id': 0, })
        self.assertEquals(resolve(url).func, view_talao)
