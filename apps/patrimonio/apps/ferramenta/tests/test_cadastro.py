from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


class YourTestClass(TestCase):

    def setUp(self) -> None:
        user = get_user_model()
        self.user = user.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        self.group = Group(
            name="patrimonio"
        )
        self.group.save()

    def test_usuario_nao_autenticado(self):
        response = self.client.get('/patrimonio/cadastros/ferramenta/')
        self.assertEqual(response.status_code, 302)

    def test_usuario_autenticado_sem_permissao(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get('/patrimonio/cadastros/ferramenta/')
        self.assertEqual(response.status_code, 302)

    def test_usuario_autenticado_com_permissao(self):
        self.client.login(username='temporary', password='temporary')
        self.user.groups.add(self.group)

        response = self.client.get('/patrimonio/cadastros/ferramenta/')
        self.assertEqual(response.status_code, 200)
