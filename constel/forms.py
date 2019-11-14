from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class FormCadastraUsuario(UserCreationForm):
    """
    Formulário de cadastro de novo usuário.
    Cadastra usuários inativos, o adm deve validar os usuários!
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
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class FormLogin(forms.Form):
    """
    Formulário de login de usuário
    """

    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    widgets = {
        'password': forms.PasswordInput(),
    }
