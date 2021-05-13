from datetime import date

from django import forms
from django.contrib.auth.models import User

from constel.forms import DateInput
from . import services
from .models import Km


class KmForm(forms.Form):

    km = forms.FloatField(label="Quilometragem", required=True)

    def __init__(self, km_id=None, user_id=None, gestor_id=None, *args, **kwargs):
        super(KmForm, self).__init__(*args, **kwargs)

        self.km_id = km_id
        self.user_id = user_id
        self.gestor_id = gestor_id

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        form_data = super(KmForm, self).clean()

        if form_data["km"] <= 0:
            self.errors["km"] = ["Não é possível registrar quilometragem nula ou negativa"]

        if not services.is_team(self.user_id, self.gestor_id):
            self.errors["km"] = ["Este colaborador não pertence à sua equipe."]

        verify, km_inicial = services.is_final_gte_initial(self.km_id, form_data["km"])
        if not verify:
            self.errors["km"] = [
                "A quilometragem final deve ser maior ou igual a inicial.",
                f"Quilometragem inicial: {km_inicial} km"
            ]

        return form_data


class RegistroForm(forms.Form):

    funcionario = forms.CharField(label="Funcionário", required=True)
    data = forms.DateField(widget=DateInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(RegistroForm, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        form_data = super(RegistroForm, self).clean()

        if not services.is_km_register(form_data.get("funcionario"), form_data.get("data")):
            self.errors["data"] = ["Não existe registro"]

        return form_data


class EditaRegistroForm(forms.ModelForm):

    class Meta:
        model = Km
        fields = ('km_initial', 'km_final')

    def __init__(self, *args, **kwargs):
        super(EditaRegistroForm, self).__init__(*args, **kwargs)

        self.fields['km_initial'].label = 'Quilometragem incial'
        self.fields['km_final'].label = 'Quilometragem final'

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        form_data = super(EditaRegistroForm, self).clean()

        verify, km_inicial = services.is_final_gte_initial(self.instance.id, self.cleaned_data["km_final"])
        print(self.instance.id)
        if not verify:

            self.errors["km_final"] = [
                "A quilometragem final deve ser maior ou igual a inicial.",
                f"Quilometragem inicial: {km_inicial} km"
            ]

        return form_data


class RegistraFaltaForm(forms.Form):

    funcionario = forms.CharField(label="Colaborador", required=True)
    data = forms.DateField(widget=DateInput(), required=False, initial=date.today().isoformat())

    def __init__(self, *args, **kwargs):
        super(RegistraFaltaForm, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        form_data = super(RegistraFaltaForm, self).clean()

        if not User.objects.filter(username=form_data.get("funcionario")).exists():
            self.errors["funcionario"] = ["Este colaborador não está cadastrado no sistema"]

        if services.is_km_register(form_data.get("funcionario"), form_data.get("data")):
            self.errors["data"] = ["Este colaborador já possui registro nesta data"]

        return form_data
