from django import forms
from django.contrib.auth.models import User

from apps.web_gc.models import Talao, Vale, EntregaTalao, EntregaVale, Combustivel


class FormTalao(forms.ModelForm):
    """
    Formulário de cadstro de novos talões
    """

    vale_inicial = forms.IntegerField(
        min_value=10000,
        max_value=999999,
        label='Vale inicial',
        help_text='Número do primeiro vale do talão'
    )
    vale_final = forms.IntegerField(
        min_value=10000,
        max_value=999999,
        label='Vale final',
        help_text='Número do último vale do talão'
    )

    class Meta:
        model = Talao
        fields = ['talao', ]


class FormEntregaTalao(forms.ModelForm):
    """
    Formulário de entrega de talões cadastrados
    """

    class Meta:
        model = EntregaTalao
        fields = ['talao', 'user_to', ]

    def __init__(self, *args, **kwargs):
        # Redefinição dos filtros para busca de objetos nas models para exibir apenas talões aptos para entrega
        super(FormEntregaTalao, self).__init__(*args, **kwargs)
        self.fields['talao'].queryset = Talao.objects.filter(status=0)
        users = User.objects.filter(is_active=True)
        users_name = [(i.id, '%s - %s %s' % (i.username, i.first_name, i.last_name)) for i in users]
        self.fields['user_to'] = forms.ChoiceField(
            choices=users_name,
            label='Funcionário',
            help_text='Funcionário que solicitou o talão de combustível.')

    def clean(self):
        self.cleaned_data['user_to'] = User.objects.get(id=int(self.cleaned_data['user_to']))


class FormEntregaVale(forms.ModelForm):
    """
    Formulário de entrega de vales cadastrados
    """

    class Meta:
        model = EntregaVale
        fields = ['vale', 'user_to', 'combustivel', 'valor', 'observacao', ]

    def __init__(self, user, *args, **kwargs):
        self.user = user
        # Redefinição dos filtros para busca de objetos nas models para exibir apenas vales aptos para entrega
        super(FormEntregaVale, self).__init__(*args, **kwargs)
        # Filtrando apenas vales que estao com o usuário logado
        self.fields['vale'].queryset = Vale.objects.filter(talao__talao_entrega__user_to=self.user, status=1)
        # Filtrando para permitir entrega apenas para funcionários que estão ativos nos sistema
        users = User.objects.filter(is_active=True)
        users_name = [(i.id, '%s - %s %s' % (i.username, i.first_name, i.last_name)) for i in users]
        self.fields['user_to'] = forms.ChoiceField(
            choices=users_name,
            label='Funcionário',
            help_text='Funcionário que solicitou o vale de combustível.')

    def clean(self):
        self.cleaned_data['user_to'] = User.objects.get(id=int(self.cleaned_data['user_to']))


class FormCadastraCombustivel(forms.ModelForm):
    """
    Formulário de cadastro de novos combustíveis
    """

    class Meta:
        model = Combustivel
        fields = '__all__'
