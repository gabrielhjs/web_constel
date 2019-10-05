from django.test import TestCase
from django.db.transaction import atomic

from .models import Talao


class TalaoTestCase(TestCase):

    def test_invalidos(self):
        """Testando se é possível cadastrar talão com formas inválidas"""
        invalidos = [
            'a',
            'asdasd',
            '0',
            '123',
            '012as',
        ]
        for talao in invalidos:
            try:
                with atomic():
                    w = Talao.objects.create(talao=talao)
                    w.save()
            except:
                pass
            else:
                self.fail('Cadastrou um Talão inválido: %s' % talao)

    def test_validos(self):
        """Testando se é possível cadastrar talão com formas válidas"""
        validos = [
            '000000',
            '123456',
        ]
        for talao in validos:
            try:
                with atomic():
                    Talao.objects.create(talao=talao)
            except ValueError:
                self.fail('Não cadastrou um Talão válido: %s' % talao)
