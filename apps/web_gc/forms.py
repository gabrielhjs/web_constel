from django import forms

from apps.web_gc.models import Talao, EntregaTalao, EntregaVale


class FormTalao(forms.ModelForm):
    vale_inicial = forms.IntegerField(min_value=10000, max_value=999999)
    vale_final = forms.IntegerField(min_value=10000, max_value=999999)

    class Meta:
        model = Talao
        fields = ['talao', ]


class FormEntregaTalao(forms.ModelForm):
    class Meta:
        model = EntregaTalao
        fields = '__all__'


class FormEntregaVale(forms.ModelForm):
    class Meta:
        model = EntregaVale
        fields = '__all__'
