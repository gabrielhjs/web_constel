from django import forms

from .models import *


class FormCadastraModelo(forms.ModelForm):

    class Meta:
        model = Modelo
        fields = ['nome', 'descricao', ]


class FormCadastraSecao(forms.ModelForm):

    class Meta:
        model = Secao
        fields = ['nome', 'descricao', ]
