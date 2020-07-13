from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Veiculo


class FormCadastraUsuario(UserCreationForm):
    """
    Formulário de cadastro de novo usuário ativo, exige senha.
    """

    username = forms.IntegerField(
        required=True,
        label='Matrícula',
        widget=forms.TextInput(attrs={'placeholder': 'sua matrícula (crachá)'}),
    )
    first_name = forms.CharField(
        max_length=30,
        label='Nome',
        widget=forms.TextInput(attrs={'placeholder': 'obrigatório'}),
    )
    last_name = forms.CharField(
        max_length=100,
        label='Sobrenome',
        widget=forms.TextInput(attrs={'placeholder': 'obrigatório'}),
    )
    email = forms.EmailField(
        max_length=254,
        widget=forms.TextInput(attrs={'placeholder': 'Informe um endereço válido de email'}),
    )
    modelo = forms.CharField(
        max_length=30,
        required=False,
        label='Modelo do veículo',
        widget=forms.TextInput(attrs={'placeholder': 'obrigatório'}),
    )
    placa = forms.CharField(
        max_length=8,
        required=False,
        label='Placa do veículo',
        widget=forms.TextInput(attrs={'placeholder': 'obrigatório'}),
    )
    cor = forms.CharField(
        max_length=100,
        required=False,
        label='Cor do veículo',
        widget=forms.TextInput(attrs={'placeholder': 'obrigatório'}),
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super(FormCadastraUsuario, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})


class FormCadastraUsuarioPassivo(forms.ModelForm):
    """
    Formulário de cadastro de novo usuário passivo. Não exige senha,
    serve para cadastrar usuários que não necesstam logar no sistema.
    """

    username = forms.IntegerField(
        required=True,
        label='Matrícula',
        widget=forms.TextInput(attrs={'placeholder': 'Insira o número da sua matrícula (crachá)'}),
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Obrigatório'}),
        label='Nome'
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Obrigatório'}),
        label='Sobrenome'
    )
    email = forms.EmailField(
        max_length=254,
        widget=forms.TextInput(attrs={'placeholder': 'Informe um endereço válido de email'}),
    )
    modelo = forms.CharField(
        max_length=30,
        label='Modelo do veículo',
        widget=forms.TextInput(attrs={'placeholder': 'Obrigatório'}),
    )
    placa = forms.CharField(
        max_length=8,
        label='Placa do veículo',
        widget=forms.TextInput(attrs={'placeholder': 'Obrigatório'}),
    )
    cor = forms.CharField(
        max_length=100,
        label='Cor do veículo',
        widget=forms.TextInput(attrs={'placeholder': 'Obrigatório'}),
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)

    def __init__(self, *args, **kwargs):
        super(FormCadastraUsuarioPassivo, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})


class FormCadastrarVeiculo(forms.ModelForm):
    """
    Formulário de cadastro de veículos de funcionários existentes
    """

    class Meta:
        model = Veiculo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(FormCadastrarVeiculo, self).__init__(*args, **kwargs)

        users = User.objects.filter(is_active=True).order_by('first_name', 'last_name')
        users_name = [(i.id, '%s - %s %s' % (i.username, i.first_name.title(), i.last_name.title())) for i in users]
        self.fields['user'] = forms.ChoiceField(choices=users_name, label='Beneficiário')

        self.fields['modelo'].widget = forms.TextInput(attrs={'placeholder': 'Modelo do veículo'})
        self.fields['placa'].widget = forms.TextInput(attrs={'placeholder': 'Placa do veículo'})
        self.fields['cor'].widget = forms.TextInput(attrs={'placeholder': 'Cor do veículo'})

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        self.cleaned_data['user'] = User.objects.get(id=int(self.cleaned_data['user']))


class FormLogin(forms.Form):
    """
    Formulário de login de usuário
    """

    username = forms.CharField(max_length=150, label='Matrícula')
    password = forms.CharField(widget=forms.PasswordInput)

    widgets = {
        'password': forms.PasswordInput(),
    }


class FormFuncionario(forms.Form):
    """
    Formulário que permite selecionar um funcionário
    """

    funcionario = forms.CharField(
        label='Funcionário',
        help_text='Insira alguma informação do funcionário',
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(FormFuncionario, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})


class DateInput(forms.DateInput):
    """
    Widget para inserir calendário nos formulários com datas
    """
    input_type = 'date'


class FormDataInicialFinalFuncionario(forms.Form):
    """
    Formulário que permite selecionar um funcionário, uma data inicial e uma final
    """

    funcionario = forms.CharField(
        label='Funcionário',
        help_text='Insira alguma informação do funcionário',
        required=False
    )
    data_inicial = forms.DateField(widget=DateInput(), required=False)
    data_final = forms.DateField(widget=DateInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(FormDataInicialFinalFuncionario, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        form_data = self.cleaned_data

        if form_data['data_inicial'] >= form_data['data_final']:
            self.errors['data_inicial'] = ['A data inicial não pode ser mais recente que a data final']

        return form_data


class FormDataInicialFinal(forms.Form):
    """
    Formulário que permite selecionar uma data inicial e uma final
    """

    data_inicial = forms.DateField(widget=DateInput(), required=False)
    data_final = forms.DateField(widget=DateInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(FormDataInicialFinal, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        form_data = self.cleaned_data

        if form_data['data_inicial'] >= form_data['data_final']:
            self.errors['data_inicial'] = ['A data inicial não pode ser mais recente que a data final']

        return form_data


class FormFiltraQ(forms.Form):
    """
    Formulário que permite filtrar um talao
    """

    q = forms.CharField(
        label='Filtrar por',
        required=False
    )

    def __init__(self, descricao='', *args, **kwargs):
        super(FormFiltraQ, self).__init__(*args, **kwargs)

        self.fields['q'].widget = forms.TextInput(attrs={'placeholder': descricao})

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})


class FormFiltraQData(forms.Form):
    """
    Formulário que permite filtrar por algum parametro especificado e por data
    """

    q = forms.CharField(
        label='Filtrar por',
        required=False
    )
    data_inicial = forms.DateField(widget=DateInput(), required=False)
    data_final = forms.DateField(widget=DateInput(), required=False)

    def __init__(self, descricao='', *args, **kwargs):
        super(FormFiltraQData, self).__init__(*args, **kwargs)

        self.fields['q'].widget = forms.TextInput(attrs={'placeholder': descricao})

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        super(FormFiltraQData, self).clean()
        form_data = self.cleaned_data

        if form_data['data_inicial'] >= form_data['data_final']:
            self.errors['data_inicial'] = ['A data inicial não pode ser mais recente que a data final']

        return form_data
