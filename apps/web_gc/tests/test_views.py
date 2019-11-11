from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Talao, Vale


class TestViews(TestCase):
    """
    Testes de funcionamento das Views, e de seus formulários
    """

    def setUp(self):
        """
        Contexto para validar os testes
        :return: constexto para testes
        """

        self.user = get_user_model().objects.create_superuser('temporary', 'temporary@gmail.com', 'temporary')
        self.url = reverse('cadastro_talao')

    def test_view_cadastrar_talao_POST_user_invalid(self):
        """
        Teste de funcionário não logado enviando POST
        :return: Deve redirecionar para tela de login e não deve registrar os objetos nas Models
        """

        response = self.client.post(
            self.url,
            {
                'vale_inicial': 10001,
                'vale_final': 10025,
                'talao': 100,
            }
        )
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/login?next=/gc/cadtalao')
        self.assertEquals(Talao.objects.count(), 0)
        self.assertEquals(Vale.objects.count(), 0)

    def test_view_cadastrar_talao_POST_user_valid(self):
        """
        Teste de funcionário (super user) logado enviando POST
        :return: Deve redirecionar para tela do gc e deve registrar os objetos nas Models
        """

        self.client.login(username='temporary', password='temporary')
        response = self.client.post(
            self.url,
            {
                'vale_inicial': 10001,
                'vale_final': 10025,
                'talao': 100,
            }
        )
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/gc')
        self.assertEquals(Talao.objects.count(), 1)
        self.assertEquals(Vale.objects.count(), 25)
