from django import forms

from .models import Material


class FormCadastraMaterial(forms.ModelForm):

    class Meta:
        model = Material
        fields = ['codigo', 'material', 'descricao', 'tipo', ]
