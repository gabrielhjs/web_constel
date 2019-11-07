from django.test import TestCase, Client
from django.urls import reverse


class TestViews(TestCase):

    def test_view_cadastrar_talao_POST(self):
        client = Client()
        response = client.post(reverse('cadastro_talao'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'web_gc/cadastro_talao.html')
