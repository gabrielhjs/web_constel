from django import forms
from django.contrib.auth.models import Group, User


class FormAssociaGrupo(forms.Form):

    grupo = forms.CharField()
    
    def __init__(self, groups='', *args, **kwargs):
        super(FormAssociaGrupo, self).__init__(*args, **kwargs)

        grupos = Group.objects.exclude(name__in=groups).exclude(name='admin').order_by('name')
        grupos_names = [(i.id, i.name.title()) for i in grupos]
        self.fields['grupo'] = forms.ChoiceField(
            choices=grupos_names,
            label='Grupo',
        )

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        super(FormAssociaGrupo, self).clean()

        self.cleaned_data['grupo'] = Group.objects.get(id=self.cleaned_data['grupo'])


class FormAssociaUsuario(forms.Form):
    user = forms.CharField()

    def __init__(self, users='', *args, **kwargs):
        super(FormAssociaUsuario, self).__init__(*args, **kwargs)

        users = User.objects.filter(
            user_type__is_passive=False,
            is_active=True
        ).exclude(
            id__in=users
        ).order_by('first_name', 'last_name')

        users_list = [(i.id, f'{i.username} - {i.first_name} {i.last_name}'.title()) for i in users]
        self.fields['user'] = forms.ChoiceField(
            choices=users_list,
            label='Usuário',
        )

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        super(FormAssociaUsuario, self).clean()

        self.cleaned_data['user'] = User.objects.get(id=self.cleaned_data['user'])
