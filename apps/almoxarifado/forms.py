from django import forms

from .models import *


class FormCadastraFornecedor(forms.ModelForm):

    class Meta:
        model = Fornecedor
        fields = ['nome', 'cnpj', ]

    def __init__(self, *args, **kwargs):
        super(FormCadastraFornecedor, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class' : 'form-control'})


class FormCadastraMaterial(forms.ModelForm):

    class Meta:
        model = Material
        fields = ['codigo', 'material', 'descricao', 'tipo', ]

    def __init__(self, *args, **kwargs):
        super(FormCadastraMaterial, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class' : 'form-control'})


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

        estoque = MaterialQuantidade.objects.get(material=form_data['material']).quantidade
        retirada = form_data['quantidade']

        if (estoque - retirada) < 0:
            self._errors['quantidade'] = ['Não há esta quantidade de material disponível em estoque!']

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

    material = forms.CharField(label='Filtrar por', help_text='Insira alguma informação do material', required=False)
