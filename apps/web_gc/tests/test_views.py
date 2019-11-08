from django.test import TestCase, Client
from django.urls import reverse

from ..models import Talao


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.url_cadastro_talao = reverse('cadastro_talao')

    def test_view_cadastrar_talao_POST(self):
        response = self.client.post(
            self.url_cadastro_talao,
            {
                'vale_inicial': 10000,
                'vale_final': 10000,
                'talao': 100,
            }
        )

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Talao.objects.count(), 1)
