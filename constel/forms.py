from django import forms


class FormCadastraUsuario(forms.Form):
    """
    Formulário de cadastro de novo usuário.
    Cadastra usuários inativos, o adm deve validar os usuários!
    """

    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    def clean(self):
        cleaned_data = super(FormCadastraUsuario, self).clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError(
                "A senha não confere"
            )


class FormLogin(forms.Form):
    """
    Formulário de login de usuário
    """

    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    widgets = {
        'password': forms.PasswordInput(),
    }
