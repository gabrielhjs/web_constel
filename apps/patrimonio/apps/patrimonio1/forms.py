from django import forms
from django.core.exceptions import ValidationError

from apps.almoxarifado.apps.cont.forms import NonstickyCharfield

from .models import *


class FormCadastraPatrimonio(forms.ModelForm):

    class Meta:
        model = Patrimonio
        fields = ['nome', 'descricao', ]

    def __init__(self, *args, **kwargs):
        super(FormCadastraPatrimonio, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})


class FormEntradaPatrimonio1(forms.Form):

    codigo = forms.CharField(required=True, widget=NonstickyCharfield())

    def __init__(self, *args, **kwargs):
        super(FormEntradaPatrimonio1, self).__init__(*args, **kwargs)

        self.fields['codigo'].widget.attrs.update(
            {'autofocus': 'autofocus', 'required': 'required'}
        )

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})


class FormEntradaPatrimonio2(forms.Form):

    patrimonio = None
    valor = forms.FloatField(
        required=True,
        label='Valor agregado (R$)',
    )

    def __init__(self, *args, **kwargs):
        super(FormEntradaPatrimonio2, self).__init__(*args, **kwargs)

        patrimonio_itens = Patrimonio.objects.all().order_by('nome', 'descricao')
        patrimonio_lista = [(i.id, i.nome) for i in patrimonio_itens]

        self.fields['patrimonio'] = forms.ChoiceField(
            choices=patrimonio_lista,
            label='Modelo',
            required=True,
        )

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        super(FormEntradaPatrimonio2, self).clean()

        self.cleaned_data['patrimonio'] = Patrimonio.objects.get(id=int(self.cleaned_data['patrimonio']))


class FormSaidaPatrimonio(forms.Form):

    patrimonio = forms.CharField()
    user_to = forms.CharField()
    observacao = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'Observação de saída do patrimônio'}
        ),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(FormSaidaPatrimonio, self).__init__(*args, **kwargs)

        patrimonio = PatrimonioId.objects.filter(status=0).order_by('patrimonio__nome', 'codigo')
        patrimonio_lista = [(i.id, f'{i.codigo} | {i.patrimonio.nome}') for i in patrimonio]
        self.fields['patrimonio'] = forms.ChoiceField(
            choices=patrimonio_lista,
            label='Patrimônio',
            required=True,
        )

        users = User.objects.filter(is_active=True).order_by('first_name', 'last_name')
        users_name = [(i.id, '%s - %s %s' % (i.username, i.first_name.title(), i.last_name.title())) for i in users]
        self.fields['user_to'] = forms.ChoiceField(
            choices=users_name,
            label='Funcionário',
            required=True,
        )

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        super(FormSaidaPatrimonio, self).clean()

        self.cleaned_data['patrimonio'] = PatrimonioId.objects.get(id=int(self.cleaned_data['patrimonio']))
        self.cleaned_data['user_to'] = User.objects.get(id=int(self.cleaned_data['user_to']))
