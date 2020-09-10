from django import forms
from django.contrib.auth.models import User

from .models import Item
from apps.almoxarifado.models import Material, MaterialQuantidade, Fornecedor
from ..cont.models import Ont, OntAplicado


class FormCria(forms.Form):

    user_to = forms.CharField(
        label='Funcionário',
        widget=forms.TextInput(attrs={'placeholder': 'Insira a matrícula do funcionário'}),
    )

    def __init__(self, *args, **kwargs):
        super(FormCria, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        form_data = self.cleaned_data
        if User.objects.filter(username=form_data['user_to'], is_active=True).exists():
            form_data['user_to'] = User.objects.get(username=form_data['user_to'])

        else:
            self.errors['user_to'] = ['Este usuário não é válido!']

        return form_data


class FormInsere(forms.Form):

    quantidade = forms.IntegerField(
        widget=forms.TextInput(attrs={'placeholder': 'Insira quantidade'}),
    )
    material = forms.IntegerField(
        label='Código',
        widget=forms.TextInput(attrs={'placeholder': 'Insira o código do material'}),
    )

    def __init__(self, user_to, *args, **kwargs):
        super(FormInsere, self).__init__(*args, **kwargs)
        self.user_to = user_to

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})

        self.fields['material'].queryset = Material.objects.filter(
            quantidade__quantidade__gt=0
        ).order_by('material')

        self.fields['quantidade'].widget.attrs.update(
            {'autofocus': 'autofocus', 'required': 'required'}
        )

    def clean(self):
        form_data = self.cleaned_data

        if Material.objects.filter(codigo=form_data['material']).exists():
            form_data['material'] = Material.objects.get(codigo=form_data['material'])

            estoque = MaterialQuantidade.objects.get(material=form_data['material']).quantidade
            if Item.objects.filter(lista__user_to__username=self.user_to, material=form_data['material']).exists():
                lista = Item.objects.get(
                    lista__user_to__username=self.user_to,
                    material=form_data['material'],
                ).quantidade
            else:
                lista = 0
            
            retirada = form_data['quantidade']

            if (estoque - retirada - lista) < 0:
                self._errors['quantidade'] = ['Não há quantidade disponível em estoque! estoque: (%d)' % estoque]

            if Item.objects.filter(material=form_data['material'], lista__user_to__username=self.user_to).exists():
                lista = Item.objects.get(
                    material=form_data['material'],
                    lista__user_to__username=self.user_to
                ).quantidade

            else:
                lista = 0

            if (lista + retirada) < 0:
                self._errors['quantidade'] = ['Não é permitido retirada de quantidades negativas de material!']

        else:
            self.errors['material'] = ['Este código de material não está cadastrado!']

        return form_data


class FormOntInsere(forms.Form):

    serial = forms.CharField(label='Código', help_text='Código da ONT a ser inserida na lista')

    def __init__(self, user_to, *args, **kwargs):
        super(FormOntInsere, self).__init__(*args, **kwargs)
        self.user_to = user_to

        self.fields['serial'].widget.attrs.update(
            {'autofocus': 'autofocus', 'required': 'required'}
        )

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        form_data = self.cleaned_data
        serial = form_data['serial'].upper()

        if Ont.objects.filter(codigo=serial).exists():
            form_data['serial'] = Ont.objects.get(codigo=serial)

            if form_data['serial'].status == 2:
                aplicado = OntAplicado.objects.filter(ont__codigo=serial).latest('data')
                self.errors['serial'] = [
                    f'Ont está aplicada no contrato {aplicado.cliente.contrato}, ' +
                    'deve ser inserida no estoque para registrar nova saída'
                ]

        else:
            self.errors['serial'] = ['Ont não cadastrada no sistema, cadastre-a para registrar a saída']

        return form_data


class FormOntDefeitoFornecedor(forms.Form):

    fornecedor = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(FormOntDefeitoFornecedor, self).__init__(*args, **kwargs)

        fornecedor = Fornecedor.objects.all().order_by('nome')
        fornecedor_name = [(i.id, f'{i.cnpj} - {i.nome.title()}') for i in fornecedor]
        self.fields['fornecedor'] = forms.ChoiceField(
            choices=fornecedor_name,
            label='Fornecedor',
        )

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        form_data = self.cleaned_data

        form_data['fornecedor'] = Fornecedor.objects.get(id=form_data['fornecedor'])

        return form_data
