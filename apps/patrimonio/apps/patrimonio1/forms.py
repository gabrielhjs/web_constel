from django import forms
from django.core.exceptions import ValidationError

from .models import *


class FormCadastraPatrimonio(forms.ModelForm):

    class Meta:
        model = Patrimonio
        fields = ['nome', 'descricao', ]

    def __init__(self, *args, **kwargs):
        super(FormCadastraPatrimonio, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})


class FormEntradaPatrimonio(forms.ModelForm):

    class Meta:
        model = PatrimonioEntrada
        fields = ['patrimonio', 'codigo', 'valor', 'observacao', ]

    def __init__(self, *args, **kwargs):
        super(FormEntradaPatrimonio, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})

    def clean_codigo(self):
        codigo = self.cleaned_data['codigo']
        if PatrimonioEntrada.objects.filter(codigo=codigo, status=0).exists():
            raise ValidationError('Este objeto já se encontra no estoque do patrimônio!')

        return codigo


class FormSaidaPatrimonio(forms.ModelForm):

    class Meta:
        model = PatrimonioSaida
        fields = ['entrada', 'user_to', 'observacao', ]

    def __init__(self, *args, **kwargs):
        super(FormSaidaPatrimonio, self).__init__(*args, **kwargs)
        self.fields['entrada'].queryset = PatrimonioEntrada.objects.filter(status=0).order_by('patrimonio', 'codigo')
        users = User.objects.filter(is_active=True).order_by('first_name', 'last_name')
        users_name = [(i.id, '%s - %s %s' % (i.username, i.first_name.title(), i.last_name.title())) for i in users]
        self.fields['user_to'] = forms.ChoiceField(
            choices=users_name,
            label='Funcionário',
        )

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        self.cleaned_data['user_to'] = User.objects.get(id=int(self.cleaned_data['user_to']))
