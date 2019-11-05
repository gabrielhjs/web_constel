from django import forms


class FormCadastraUsuario(forms.Form):
    """
    Formulário de cadastro de novo usuário.
    Cadastra usuários inativos, o adm deve validar os usuários!
    """
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()


class FormLogin(forms.Form):
    """
    Formulário de login de usuário
    """
    widgets = {
        'password': forms.PasswordInput(),
    }
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
