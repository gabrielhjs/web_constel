from django import forms
from django.contrib.auth.models import User

from apps.web_gc.models import Talao, Vale, EntregaTalao, EntregaVale, Combustivel


class FormTalao(forms.ModelForm):
    vale_inicial = forms.IntegerField(min_value=10000, max_value=999999)
    vale_final = forms.IntegerField(min_value=10000, max_value=999999)

    class Meta:
        model = Talao
        fields = ['talao', ]


class FormEntregaTalao(forms.ModelForm):

    class Meta:
        model = EntregaTalao
        fields = ['talao', 'to_user', ]

    def __init__(self, *args, **kwargs):
        super(FormEntregaTalao, self).__init__(*args, **kwargs)
        self.fields['talao'].queryset = Talao.objects.filter(status=0)
        self.fields['to_user'].queryset = User.objects.filter(is_active=True)


class FormEntregaVale(forms.ModelForm):
    class Meta:
        model = EntregaVale
        fields = ['vale', 'to_user', 'combustivel', 'valor', 'observacao', ]

    def __init__(self, *args, **kwargs):
        super(FormEntregaVale, self).__init__(*args, **kwargs)
        self.fields['vale'].queryset = Vale.objects.filter(status=1)
        self.fields['to_user'].queryset = User.objects.filter(is_active=True)


class FormCadastraCombustivel(forms.ModelForm):
    class Meta:
        model = Combustivel
        fields = '__all__'
