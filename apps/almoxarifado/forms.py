from typing import overload
from django import forms

from .models import *


class FormCadastraFornecedor(forms.ModelForm):

    class Meta:
        model = Fornecedor
        fields = ['nome', 'cnpj', ]

    def __init__(self, *args, **kwargs):
        super(FormCadastraFornecedor, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})


class FormCadastraMaterial(forms.ModelForm):

    class Meta:
        model = Material
        fields = ['codigo', 'material', 'descricao', 'tipo', ]

    def __init__(self, *args, **kwargs):
        super(FormCadastraMaterial, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})


class FormEntradaMaterial(forms.ModelForm):

    class Meta:
        model = MaterialEntrada
        fields = ['material', 'fornecedor', 'quantidade', 'observacao']

    def __init__(self, *args, **kwargs):
        super(FormEntradaMaterial, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})


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


class FormSaidaMateriais1(forms.Form):

    user_to = forms.CharField(label='Funcionário', help_text='Funcionário que está solicitando o material')

    def clean(self):
        form_data = self.cleaned_data
        if User.objects.filter(username=form_data['user_to'], is_active=True).exists():
            form_data['user_to'] = User.objects.get(username=form_data['user_to'])

        else:
            self.errors['user_to'] = ['Este usuário não é válido!']

        return form_data


class FormSaidaMateriais2(forms.ModelForm):

    class Meta:
        model = MaterialSaida
        fields = ['material', 'quantidade', 'observacao', ]

    def __init__(self, *args, **kwargs):
        super(FormSaidaMateriais2, self).__init__(*args, **kwargs)

        self.fields['material'].queryset = Material.objects.filter(
            quantidade__quantidade__gt=0
        ).order_by('material')

    def clean(self):
        form_data = self.cleaned_data

        if not Material.objects.get(codigo=form_data['material']).exists():
            self._errors['material'] = ['Material não cadastrado no sistema!']

            return form_data

        if not MaterialQuantidade.objects.get(codigo=form_data['material']).exists():
            self._errors['material'] = ['Não há registro de aquisição deste material!']

            return form_data

        estoque = MaterialQuantidade.objects.get(material__codigo=form_data['material']).quantidade
        retirada = form_data['quantidade']

        if (estoque - retirada) < 0:
            self._errors['quantidade'] = [f'Não há quantidade de material disponível em estoque! (estoque: {estoque})']

        return form_data


class FormCadastraUsuarioPassivo(forms.ModelForm):
    """
    Formulário de cadastro de novo usuário passivo. Não exige senha,
    serve para cadastrar usuários que não necesstam logar no sistema.
    """

    username = forms.IntegerField(
        required=True,
        label='Matrícula',
        help_text='Insira o número da sua matrícula (crachá)'
    )
    first_name = forms.CharField(max_length=30, help_text='Obrigatório.', label='Nome')
    last_name = forms.CharField(max_length=100, help_text='Obrigatório.', label='Sobrenome')
    email = forms.EmailField(max_length=254, help_text='Obrigatório. Informe um endereço válido de email.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)


class FormMaterial(forms.Form):
    """
    Formulário que permite filtrar um material
    """

    material = forms.CharField(
        label='Filtrar por',
        widget=forms.TextInput(attrs={'placeholder': 'código ou nome'}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(FormMaterial, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})


class FormFornecedor(forms.Form):
    """
    Formulário que permite filtrar um fornecedor
    """

    q = forms.CharField(
        label='Filtrar por',
        widget=forms.TextInput(attrs={'placeholder': 'cnpj|nome|material'}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(FormFornecedor, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})


class FormMaterialEdita(forms.ModelForm):

    class Meta:
        model = Material
        fields = ['material', 'descricao', 'tipo', 'status']

    def __init__(self, *args, **kwargs):
        super(FormMaterialEdita, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        super(FormMaterialEdita, self).clean()

        form_data = self.cleaned_data
        model_instance = self.instance

        if not form_data["status"] and model_instance.quantidade.quantidade != 0:
            self.errors["status"] = [
                "Você só pode desabilitar materiais que não possuem estoque",
                f"Estoque atual: {model_instance.quantidade.quantidade}"
            ]


class FormMaterialFornecedorPrazo(forms.ModelForm):

    class Meta:
        model = MaterialFornecedorPrazo
        fields = ['fornecedor', 'dias', 'dias_uteis']

    def __init__(self, *args, **kwargs):
        super(FormMaterialFornecedorPrazo, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})
