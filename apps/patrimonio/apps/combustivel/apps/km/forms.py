from django import forms

from . import services


class KmForm(forms.Form):

    km = forms.FloatField(label="Quilometragem", required=True)

    def __init__(self, user_id=None, gestor_id=None, *args, **kwargs):
        super(KmForm, self).__init__(*args, **kwargs)

        self.user_id = user_id
        self.gestor_id = gestor_id

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        form_data = super(KmForm, self).clean()

        if form_data["km"] <= 0:
            self.errors["km"] = ["Não é possível registrar entrada futura."]

        if not services.is_team(self.user_id, self.gestor_id):
            self.errors["km"] = ["Este colaborador não pertence à sua equipe."]

        return form_data
