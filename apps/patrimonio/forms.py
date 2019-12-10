from django import forms

from .models import *


class FormCadastraFerramenta(forms.ModelForm):

    class Meta:
        model = Ferramenta
        fields = ['nome', 'descricao', ]


class FormCadastraPatrimonio(forms.ModelForm):

    class Meta:
        model = Patrimonio
        fields = ['nome', 'descricao', ]


class FormEntradaFerramenta(forms.ModelForm):

    class Meta:
        model = FerramentaEntrada
        fields = ['ferramenta', 'quantidade', 'valor', 'observacao', ]
