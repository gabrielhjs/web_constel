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
            self.errors["km"] = ["Não é possível registrar quilometragem nula ou negativa"]

        if not services.is_team(self.user_id, self.gestor_id):
            self.errors["km"] = ["Este colaborador não pertence à sua equipe."]

        verify, km_inicial = services.is_final_gte_initial(self.user_id, self.gestor_id, form_data["km"])
        if not verify:
            self.errors["km"] = [
                "A quilometragem final deve ser maior ou igual a inicial.",
                f"Quilometragem inicial: {km_inicial} km"
            ]

        return form_data
