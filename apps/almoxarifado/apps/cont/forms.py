from django import forms

from .models import *


class FormCadastraModelo(forms.ModelForm):

    class Meta:
        model = Modelo
        fields = ['nome', 'descricao', ]


class FormCadastraSecao(forms.ModelForm):

    class Meta:
        model = Secao
        fields = ['nome', 'descricao', ]


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

    def clean(self):
        form_data = super().clean()
        serial = form_data['serial'].upper()

        if Ont.objects.filter(codigo=serial).exists():

            if Ont.objects.get(codigo=serial).status == 0:
                self.errors['serial'] = ['Serial já em estoque']

                return form_data

        if serial.find('4857544', 0, 7) >= 0:

            if len(serial) != 16:
                self.errors['serial'] = ['Serial Huawei inválido']

                return form_data

        elif serial.find('ZNITS', 0, 5) >= 0:

            if len(serial) != 12:
                self.errors['serial'] = ['Serial Zhone inválido']

                return form_data

        else:
            self.errors['serial'] = ['Serial inválido']

            return form_data
