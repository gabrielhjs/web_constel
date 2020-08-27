from django import forms

from .models import *


class FormCadastraModelo(forms.ModelForm):

    class Meta:
        model = Modelo
        fields = ['nome', 'descricao', ]

    def __init__(self, *args, **kwargs):
        super(FormCadastraModelo, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})


class FormCadastraSecao(forms.ModelForm):

    class Meta:
        model = Secao
        fields = ['nome', 'descricao', ]

    def __init__(self, *args, **kwargs):
        super(FormCadastraSecao, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})


class FormEntradaOnt1(forms.Form):

    modelo = forms.ChoiceField()
    secao = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(FormEntradaOnt1, self).__init__(*args, **kwargs)

        modelos = Modelo.objects.all().order_by('nome')
        modelos_name = [(i.id, i.nome.upper()) for i in modelos]
        self.fields['modelo'] = forms.ChoiceField(
            choices=modelos_name,
            label='Modelo',
            help_text='Modelo das ONT\'s a serem inseridas',
        )

        secoes = Secao.objects.all().order_by('nome')
        secoes_name = [(i.id, i.nome.upper()) for i in secoes]
        self.fields['secao'] = forms.ChoiceField(
            choices=secoes_name,
            label='Seção',
            help_text='Atividade de destino das ONT\'s a serem inseridas',
        )

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})


class NonstickyCharfield(forms.TextInput):
    """Custom text input widget that's "non-sticky"
    (i.e. does not remember submitted values).
    """
    def get_context(self, name, value, attrs):
        value = None  # Clear the submitted value.

        return super().get_context(name, value, attrs)


class FormEntradaOnt2(forms.Form):

    serial = forms.CharField(required=True, widget=NonstickyCharfield())

    def __init__(self, *args, **kwargs):
        super(FormEntradaOnt2, self).__init__(*args, **kwargs)

        self.fields['serial'].widget.attrs.update(
            {'autofocus': 'autofocus', 'required': 'required'}
        )

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        form_data = super().clean()
        serial = form_data['serial'].upper()

        if serial.find('4857544', 0, 7) >= 0:

            if len(serial) != 16:
                self.errors['serial'] = ['Serial de Ont Huawei inválido']

                return form_data

        elif serial.find('ZNTS', 0, 5) >= 0:

            if len(serial) != 12:
                self.errors['serial'] = ['Serial de Ont Zhone inválido']

                return form_data

        else:
            self.errors['serial'] = ['Serial de Ont inválido']

            return form_data


class FormOntFechamento(forms.Form):

    serial = forms.CharField(required=True, widget=NonstickyCharfield())

    def __init__(self, *args, **kwargs):
        super(FormOntFechamento, self).__init__(*args, **kwargs)

        self.fields['serial'].widget.attrs.update(
            {'autofocus': 'autofocus', 'required': 'required'}
        )

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        form_data = super().clean()
        serial = form_data['serial'].upper()

        if Ont.objects.filter(codigo=serial).exists():
            form_data['serial'] = Ont.objects.get(codigo=serial)

        else:
            self.errors['serial'] = ['Ont não cadastrada no sistema, cadastre-a para registrá-la como com defeito']

        return form_data


class FormOntManutencao1(forms.Form):

    modelo = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(FormOntManutencao1, self).__init__(*args, **kwargs)

        modelos = Modelo.objects.all().order_by('nome')
        modelos_name = [(i.id, i.nome.upper()) for i in modelos]
        self.fields['modelo'] = forms.ChoiceField(
            choices=modelos_name,
            label='Modelo',
        )

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})


class FormPswLogin(forms.Form):
    """
    Formulário de login de usuário no psw
    """

    username = forms.CharField(max_length=150, label='Chave da Copel')
    password = forms.CharField(widget=forms.PasswordInput)

    widgets = {
        'password': forms.PasswordInput(),
    }

    def __init__(self, *args, **kwargs):
        super(FormPswLogin, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})


class FormPswContrato(forms.Form):
    """
    Formulário de busca de contrato no psw
    """

    contratos = forms.CharField(
        label='Contratos',
        widget=forms.TextInput(
            attrs={'placeholder': 'Ex: 1234567,1234568, 1234569'}
        )
    )

    def __init__(self, *args, **kwargs):
        super(FormPswContrato, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})


class FormSerial(forms.Form):
    """
    Formulário de busca de serial
    """

    serial = forms.CharField(label='Serial', required=False)

    def __init__(self, *args, **kwargs):
        super(FormSerial, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})
