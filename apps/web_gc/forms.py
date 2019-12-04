from django import forms
from django.contrib.auth.models import User

from apps.web_gc.models import Talao, Vale, EntregaTalao, EntregaVale, Combustivel, Posto
from constel.models import Veiculo


class FormTalao(forms.ModelForm):
    """
    Formulário de cadstro de novos talões
    """

    vale_inicial = forms.IntegerField(
        label='Vale inicial',
        help_text='Número do primeiro vale do talão'
    )
    vale_final = forms.IntegerField(
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
        users_name = [(i.id, '%s - %s %s' % (i.username, i.first_name.title(), i.last_name.title())) for i in users]
        self.fields['user_to'] = forms.ChoiceField(
            choices=users_name,
            label='Funcionário',
            help_text='Funcionário que solicitou o talão de combustível.')

    def clean(self):
        self.cleaned_data['user_to'] = User.objects.get(id=int(self.cleaned_data['user_to']))


class FormEntregaVale1(forms.Form):
    """
    Formulário de entrega de vales cadastrados
    """

    vale = forms.ChoiceField()
    user_to = forms.ChoiceField()

    def __init__(self, user, *args, **kwargs):
        super(FormEntregaVale1, self).__init__(*args, **kwargs)
        self.user = user

        # Queryset Field vale
        vales = Vale.objects.filter(talao__talao_entrega__user_to=self.user, status=1)
        vales_name = [(i.id, '%d' % i.vale) for i in vales]
        self.fields['vale'] = forms.ChoiceField(
            choices=vales_name,
            label='Vale',
            help_text='Número do vale que será entregue.')

        # Queryset Field User_to
        self.fields['vale'].queryset = Vale.objects.filter(talao__talao_entrega__user_to=self.user, status=1)
        users = User.objects.filter(is_active=True)
        users_name = [(i.id, '%s - %s %s' % (i.username, i.first_name.title(), i.last_name.title())) for i in users]
        self.fields['user_to'] = forms.ChoiceField(
            choices=users_name,
            label='Funcionário',
            help_text='Funcionário que solicitou o vale de combustível.')


class FormEntregaVale2(forms.ModelForm):

    class Meta:
        model = EntregaVale
        fields = ['combustivel', 'valor', 'observacao', ]

    posto = forms.ChoiceField()

    def __init__(self, user_to, *args, **kwargs):
        self.user_to = user_to
        super(FormEntregaVale2, self).__init__(*args, **kwargs)
        veiculos = Veiculo.objects.filter(user=self.user_to)
        veiculos_name = [(i.id, '%s - %s - %s' % (i.modelo.title(), i.placa.upper(), i.cor.upper())) for i in veiculos]
        self.fields['veiculo'] = forms.ChoiceField(
            choices=veiculos_name,
            label='Veículo',
            help_text='Veículo que será abastecido',
            error_messages={'required': 'Campo obrigatório. Caso não haja nenhuma opção deve ser cadastrado o veículo\
                                         no menu de cadastros.'}
        )
        postos = Posto.objects.all()
        postos_name = [(i.id, '%s' % i.posto) for i in postos]
        self.fields['posto'] = forms.ChoiceField(
            choices=postos_name,
            label='Posto',
        )


class FormCadastraCombustivel(forms.ModelForm):
    """
    Formulário de cadastro de novos combustíveis
    """

    class Meta:
        model = Combustivel
        fields = '__all__'


class FormCadastraPosto(forms.ModelForm):
    """
    Formulário de cadastro de novos combustíveis
    """

    class Meta:
        model = Posto
        fields = '__all__'
