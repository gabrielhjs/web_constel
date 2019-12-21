from django import forms
from django.contrib.auth.models import User

from .models import Item
from apps.almoxarifado.models import Material, MaterialQuantidade


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

    material = forms.IntegerField(label='Código', help_text='Código do material a ser inserido na lista')
    quantidade = forms.IntegerField(initial=1)

    def __init__(self, user_to, *args, **kwargs):
        super(FormItemInsere, self).__init__(*args, **kwargs)
        self.user_to = user_to

        self.fields['material'].queryset = Material.objects.filter(
            quantidade__quantidade__gt=0
        ).order_by('material')

        self.fields['material'].widget.attrs.update(
            {'autofocus': 'autofocus', 'required': 'required'}
        )

    def clean(self):
        form_data = self.cleaned_data
        for i in form_data:
            print(i)

        if Material.objects.filter(codigo=form_data['material']).exists():
            print('adasdfsadfasdf')
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
