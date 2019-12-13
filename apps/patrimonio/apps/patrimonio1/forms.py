from django import forms

from .models import *


class FormCadastraPatrimonio(forms.ModelForm):

    class Meta:
        model = Patrimonio
        fields = ['nome', 'descricao', ]


class FormEntradaPatrimonio(forms.ModelForm):

    class Meta:
        model = PatrimonioEntrada
        fields = ['patrimonio', 'codigo', 'valor', 'observacao', ]
