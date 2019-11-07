from django.test import TestCase
from django.db.transaction import atomic

from apps.web_gc.models import Talao, Vale


class TalaoTestCase(TestCase):
    """
    Testando a Model Talao
    """

    def test_invalidos(self):
        """
        Testando se é possível cadastrar talões com formatos inválidos
        """
        invalidos = [
            'a',
            'asdasd',
            '012as',
            '100',
        ]
        for talao in invalidos:
            with atomic():
                with self.assertRaises(ValueError):
                    test = Talao(talao=talao)
                    test.save()

    def test_validos(self):
        """
        Testando se é possível cadastrar talões com formatos válidos
        """
        validos = [
            123456,
        ]
        for talao in validos:
            with atomic():
                test = Talao(talao=talao)
                test.save()


class ValeTestCase(TestCase):
    """
    Testando a Model Vale
    """

    def test_invalidos(self):
        """
        Testando se é possível cadastrar vales com formatos inválidos
        """
        invalidos = [
            'a',
            'asdasd',
            '012as',
        ]
        talao = Talao(talao=111111)
        talao.save()
        for vale in invalidos:
            with atomic():
                with self.assertRaises(ValueError):
                    test = Vale(vale=vale, talao=talao)
                    test.save()

    def test_validos(self):
        """
        Testando se é possível cadastrar vales com formatos válidos
        """
        validos = [
            123456,
        ]
        talao = Talao(talao=111111)
        talao.save()
        for vale in validos:
            with atomic():
                test = Vale(vale=vale, talao=talao)
                test.save()
