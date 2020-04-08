from django import forms
from django.contrib.auth.models import User

from .models import Item
from apps.almoxarifado.models import Material, MaterialQuantidade
from ..cont.models import Ont, OntAplicado


class FormListaCria(forms.Form):

    user_to = forms.CharField(label='Funcionário', help_text='Funcionário que está solicitando o material')

    def clean(self):
        form_data = self.cleaned_data
        if User.objects.filter(username=form_data['user_to'], is_active=True).exists():
            form_data['user_to'] = User.objects.get(username=form_data['user_to'])

        else:
            self.errors['user_to'] = ['Este usuário não é válido!']

        return form_data


class FormItemInsere(forms.Form):

    quantidade = forms.IntegerField()
    material = forms.IntegerField(label='Código', help_text='Código do material a ser inserido na lista')

    def __init__(self, user_to, *args, **kwargs):
        super(FormItemInsere, self).__init__(*args, **kwargs)
        self.user_to = user_to

        self.fields['material'].queryset = Material.objects.filter(
            quantidade__quantidade__gt=0
        ).order_by('material')

        self.fields['quantidade'].widget.attrs.update(
            {'autofocus': 'autofocus', 'required': 'required'}
        )

    def clean(self):
        form_data = self.cleaned_data

        if Material.objects.filter(codigo=form_data['material']).exists():
            form_data['material'] = Material.objects.get(codigo=form_data['material'])

            estoque = MaterialQuantidade.objects.get(material=form_data['material']).quantidade
            retirada = form_data['quantidade']

            if (estoque - retirada) < 0:
                self._errors['quantidade'] = ['Não há esta quantidade de material disponível em estoque!']

            if Item.objects.filter(material=form_data['material'], lista__user_to__username=self.user_to).exists():
                lista = Item.objects.get(
                    material=form_data['material'],
                    lista__user_to__username=self.user_to
                ).quantidade

            else:
                lista = 0

            if (lista + retirada) < 0:
                self._errors['quantidade'] = ['Não é permitido retirada de quantidades negativas de material!']

        else:
            self.errors['material'] = ['Este código de material não está cadastrado!']

        return form_data


class FormOntInsere(forms.Form):

    serial = forms.CharField(label='Código', help_text='Código da ONT a ser inserida na lista')

    def __init__(self, user_to, *args, **kwargs):
        super(FormOntInsere, self).__init__(*args, **kwargs)
        self.user_to = user_to

        self.fields['serial'].widget.attrs.update(
            {'autofocus': 'autofocus', 'required': 'required'}
        )

    def clean(self):
        form_data = self.cleaned_data
        serial = form_data['serial'].upper()

        if Ont.objects.filter(codigo=serial).exists():
            form_data['serial'] = Ont.objects.get(codigo=serial)

            if form_data['serial'].status == 2:
                aplicado = OntAplicado.objects.filter(ont__codigo=serial).latest('data')
                self.errors['serial'] = [
                    'Ont está aplicada no contrato %d, ' % aplicado.cliente /
                    'deve ser inserida no estoque para registrar nova saída'
                ]

        else:
            self.errors['serial'] = ['Ont não cadastrada no sistema, cadastre-a para registrar a saída']

        return form_data
