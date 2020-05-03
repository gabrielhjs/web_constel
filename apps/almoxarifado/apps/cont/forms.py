from django import forms

from .models import *


class FormCadastraModelo(forms.ModelForm):

    class Meta:
        model = Modelo
        fields = ['nome', 'descricao', ]

    def __init__(self, *args, **kwargs):
        super(FormCadastraModelo, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class' : 'form-control'})


class FormCadastraSecao(forms.ModelForm):

    class Meta:
        model = Secao
        fields = ['nome', 'descricao', ]

    def __init__(self, *args, **kwargs):
        super(FormCadastraSecao, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class' : 'form-control'})


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
            self.fields[key].widget.attrs.update({'class' : 'form-control'})


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
            self.fields[key].widget.attrs.update({'class' : 'form-control'})

    def clean(self):
        form_data = super().clean()
        serial = form_data['serial'].upper()

        if Ont.objects.filter(codigo=serial).exists():

            if Ont.objects.get(codigo=serial).status == 0:
                self.errors['serial'] = ['Serial de Ont já em estoque']

                return form_data

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


class FormSaidaOnt1(forms.Form):

    funcionario = forms.CharField(label='Funcionário')

    def __init__(self, *args, **kwargs):
        super(FormSaidaOnt1, self).__init__(*args, **kwargs)

        self.fields['funcionario'].widget.attrs.update(
            {'autofocus': 'autofocus', 'required': 'required'}
        )

    def clean(self):
        form_data = super().clean()
        usuario = form_data['funcionario']

        if not User.objects.filter(username=usuario).exists():
            self.errors['funcionario'] = ['Funcionário inativo ou não cadastrado no sistema']

        return form_data


class FormSaidaOnt2(forms.Form):

    serial = forms.CharField(required=True, widget=NonstickyCharfield())

    def __init__(self, *args, **kwargs):
        super(FormSaidaOnt2, self).__init__(*args, **kwargs)

        self.fields['serial'].widget.attrs.update(
            {'autofocus': 'autofocus', 'required': 'required'}
        )

    def clean(self):
        form_data = super().clean()
        serial = form_data['serial'].upper()

        if Ont.objects.filter(codigo=serial).exists():
            ont = Ont.objects.get(codigo=serial)

            if ont.status == 2:
                aplicado = OntAplicado.objects.filter(ont__codigo=serial).latest('data')
                self.errors['serial'] = [
                    'Ont está aplicada no contrato %d, ' % aplicado.cliente /
                    'deve ser inserida no estoque para registrar nova saída'
                ]

        else:
            self.errors['serial'] = ['Ont não cadastrada no sistema, cadastre-a para registrar a saída']

        return form_data
