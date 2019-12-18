from django import forms

from .models import *


class FormCadastraFornecedor(forms.ModelForm):

    class Meta:
        model = Fornecedor
        fields = ['nome', 'cnpj', ]


class FormCadastraMaterial(forms.ModelForm):

    class Meta:
        model = Material
        fields = ['codigo', 'material', 'descricao', 'tipo', ]


class FormEntradaMaterial(forms.ModelForm):

    class Meta:
        model = MaterialEntrada
        fields = ['material', 'fornecedor', 'quantidade', 'observacao']


class FormSaidaMaterial(forms.ModelForm):

    class Meta:
        model = MaterialSaida
        fields = ['user_to', 'material', 'quantidade', 'observacao', ]

    def __init__(self, *args, **kwargs):
        super(FormSaidaMaterial, self).__init__(*args, **kwargs)

        self.fields['material'].queryset = Material.objects.filter(
            quantidade__quantidade__gt=0
        ).order_by('material')

        users = User.objects.filter(is_active=True).order_by('first_name', 'last_name')
        users_name = [(i.id, '%s - %s %s' % (i.username, i.first_name.title(), i.last_name.title())) for i in users]
        self.fields['user_to'] = forms.ChoiceField(
            choices=users_name,
            label='Funcionário',
            help_text='Funcionário que solicitou o material.',
        )

    def clean(self):
        form_data = self.cleaned_data
        form_data['user_to'] = User.objects.get(id=int(form_data['user_to']))

        estoque = MaterialQuantidade.objects.get(material=form_data['material']).quantidade
        retirada = form_data['quantidade']

        if (estoque - retirada) < 0:
            self._errors['quantidade'] = ['Não há esta quantidade de material disponível em estoque!']

        return form_data
