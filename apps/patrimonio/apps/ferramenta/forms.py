from django import forms

from .models import *


class FormCadastraFerramenta(forms.ModelForm):

    class Meta:
        model = Ferramenta
        fields = ['nome', 'descricao', ]

    def __init__(self, *args, **kwargs):
        super(FormCadastraFerramenta, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})


class FormEntradaFerramenta(forms.ModelForm):

    class Meta:
        model = FerramentaEntrada
        fields = ['ferramenta', 'quantidade', 'valor', 'observacao', ]

    def __init__(self, *args, **kwargs):
        super(FormEntradaFerramenta, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})


class FormSaidaFerramenta(forms.ModelForm):

    class Meta:
        model = FerramentaSaida
        fields = ['user_to', 'ferramenta', 'quantidade', 'observacao', ]

    def __init__(self, *args, **kwargs):
        super(FormSaidaFerramenta, self).__init__(*args, **kwargs)

        self.fields['ferramenta'].queryset = Ferramenta.objects.filter(
            quantidade__quantidade__gt=0
        ).order_by('nome')

        users = User.objects.filter(is_active=True).order_by('first_name', 'last_name')
        users_name = [(i.id, '%s - %s %s' % (i.username, i.first_name.title(), i.last_name.title())) for i in users]
        self.fields['user_to'] = forms.ChoiceField(
            choices=users_name,
            label='Funcionário',
        )

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        form_data = self.cleaned_data
        form_data['user_to'] = User.objects.get(id=int(form_data['user_to']))

        estoque = FerramentaQuantidade.objects.get(ferramenta=form_data['ferramenta']).quantidade
        retirada = form_data['quantidade']

        if (estoque - retirada) < 0:
            self._errors['quantidade'] = ['Não há esta quantidade de ferramentas disponível em estoque!']

        return form_data


class FormFechamentoFerramenta(forms.Form):

    user_from = forms.CharField()
    ferramenta = forms.CharField()
    status = forms.CharField()
    quantidade = forms.IntegerField(required=True)
    observacao = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'asd'}), required=False)

    def __init__(self, *args, **kwargs):
        super(FormFechamentoFerramenta, self).__init__(*args, **kwargs)

        ferramentas = Ferramenta.objects.all().order_by('nome')
        ferramentas_lista = [(i.id, i.nome) for i in ferramentas]
        self.fields['ferramenta'] = forms.ChoiceField(
            choices=ferramentas_lista,
            label='Ferramenta',
            required=True,
        )

        self.fields['status'] = forms.ChoiceField(
            choices=FerramentaFechamento.STATUS,
            label='Status',
            required=True,
        )

        users = User.objects.filter(is_active=True).order_by('first_name', 'last_name')
        users_lista = [(i.id, '%s - %s %s' % (i.username, i.first_name.title(), i.last_name.title())) for i in users]
        self.fields['user_from'] = forms.ChoiceField(
            choices=users_lista,
            label='Funcionário',
        )

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        form_data = self.cleaned_data
        form_data['user_from'] = User.objects.get(id=int(form_data['user_from']))
        form_data['ferramenta'] = Ferramenta.objects.get(id=int(form_data['ferramenta']))

        print(form_data['user_from'])
        print(form_data['ferramenta'])

        if not FerramentaQuantidadeFuncionario.objects.filter(
            user=form_data['user_from'],
            ferramenta=form_data['ferramenta'],
            quantidade__gte=form_data['quantidade']
        ).exists():
            self._errors['quantidade'] = ['Não há essa quantidade de ferramentas na carga deste funcionário']

        return form_data


class FormEditaModeloFerramenta(forms.ModelForm):

    class Meta:
        model = Ferramenta
        fields = ('nome', 'descricao')

    def __init__(self, *args, **kwargs):
        super(FormEditaModeloFerramenta, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})
