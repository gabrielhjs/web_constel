from django import forms
from django.contrib.auth.models import Group


class FormCriaGrupo(forms.Form):

    nome = forms.CharField(max_length=255)

    def clean(self):

        if Group.objects.filter(name=self.cleaned_data['nome']).exists():
            self.errors['nome'] = ['Este grupo já existe!']


class FormAssociaGrupo(forms.Form):

    grupo = forms.CharField()
    
    def __init__(self, *args, **kwargs):
        super(FormAssociaGrupo, self).__init__(*args, **kwargs)
        grupos = Group.objects.all().order_by('name')
        grupos_names = [(i.id, i.name.title()) for i in grupos]
        self.fields['grupo'] = forms.ChoiceField(
            choices=grupos_names,
            label='Grupo',
        )
