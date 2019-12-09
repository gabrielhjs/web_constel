from django import forms

from .models import Ferramenta


class FormCadastraFerramenta(forms.ModelForm):

    class Meta:
        model = Ferramenta
        fields = ['nome', 'descricao', ]
