from django import forms
from django.contrib.auth.models import User

from .models import Talao, Vale, EntregaTalao, EntregaVale, Combustivel, Posto
from constel.models import Veiculo


class FormCadastraTalao(forms.ModelForm):
    """
    Formulário de cadstro de novos talões
    """

    vale_inicial = forms.IntegerField(
        label='Vale inicial',
        widget=forms.TextInput(attrs={'placeholder': 'Número do primeiro vale do talão'}),
    )
    vale_final = forms.IntegerField(
        label='Vale final',
        widget=forms.TextInput(attrs={'placeholder': 'Número do último vale do talão'}),
    )

    class Meta:
        model = Talao
        fields = ['talao', ]

    def __init__(self, *args, **kwargs):
        super(FormCadastraTalao, self).__init__(*args, **kwargs)

        self.fields['talao'].widget = forms.TextInput(attrs={'placeholder': 'Código numérico do talão'})

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        form_data = self.cleaned_data
        if Talao.objects.filter(talao=form_data['talao']).exists():
            self.errors['talao'] = ['Este talão já está cadastrado']

        for vale in range(form_data['vale_inicial'], form_data['vale_inicial'] + 1):
            if Vale.objects.filter(vale=vale).exists():
                self.errors['vale_final'] = ['O vale %d já está cadastrado no sistema!' % vale]

                return form_data

        return form_data


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
        self.fields['talao'].queryset = Talao.objects.filter(status=0).order_by('talao')
        users = User.objects.filter(is_active=True).order_by('first_name', 'last_name')
        users_name = [(i.id, '%s - %s %s' % (i.username, i.first_name.title(), i.last_name.title())) for i in users]
        self.fields['user_to'] = forms.ChoiceField(
            choices=users_name,
            label='Funcionário',
        )

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})

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
        vales = Vale.objects.filter(talao__talao_entrega__user_to=self.user, status=1).order_by('talao', 'vale')
        vales_name = [(i.id, '%d' % i.vale) for i in vales]
        self.fields['vale'] = forms.ChoiceField(
            choices=vales_name,
            label='Vale',
        )

        # Queryset Field User_to
        self.fields['vale'].queryset = Vale.objects.filter(talao__talao_entrega__user_to=self.user, status=1)
        users = User.objects.filter(is_active=True).order_by('first_name', 'last_name')
        users_name = [(i.id, '%s - %s %s' % (i.username, i.first_name.title(), i.last_name.title())) for i in users]
        self.fields['user_to'] = forms.ChoiceField(
            choices=users_name,
            label='Funcionário',
        )

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})


class FormEntregaVale2(forms.ModelForm):

    class Meta:
        model = EntregaVale
        fields = ['combustivel', 'valor', 'observacao', ]

    posto = forms.ChoiceField()

    def __init__(self, user_to, *args, **kwargs):
        self.user_to = user_to
        super(FormEntregaVale2, self).__init__(*args, **kwargs)
        veiculos = Veiculo.objects.filter(user=self.user_to).order_by('modelo')
        veiculos_name = [(i.id, '%s - %s - %s' % (i.modelo.title(), i.placa.upper(), i.cor.upper())) for i in veiculos]
        self.fields['veiculo'] = forms.ChoiceField(
            choices=veiculos_name,
            label='Veículo',
            error_messages={'required': 'Campo obrigatório. Caso não haja nenhuma opção deve ser cadastrado o veículo\
                                         no menu de cadastros'}
        )
        postos = Posto.objects.all().order_by('posto')
        postos_name = [(i.id, '%s' % i.posto) for i in postos]
        self.fields['posto'] = forms.ChoiceField(
            choices=postos_name,
            label='Posto',
        )

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})


class FormCadastraCombustivel(forms.ModelForm):
    """
    Formulário de cadastro de novos combustíveis
    """

    class Meta:
        model = Combustivel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(FormCadastraCombustivel, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})


class FormCadastraPosto(forms.ModelForm):
    """
    Formulário de cadastro de novos postos
    """

    class Meta:
        model = Posto
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(FormCadastraPosto, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})


class FormBuscaValeEntregue(forms.Form):
    """
    Form para a busca de vales já entregues
    """

    vale = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'placeholder': 'código numérico do vale'}))

    def __init__(self, *args, **kwargs):
        super(FormBuscaValeEntregue, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        form_data = super(FormBuscaValeEntregue, self).clean()

        if not Vale.objects.filter(vale=form_data['vale']).exists():
            self.errors['vale'] = ['Vale não encontrado']

            return form_data

        vale = Vale.objects.get(vale=form_data['vale'])

        if vale.status != 2:
            self.errors['vale'] = ['Vale NÃO consta como entregue no sistema']

            return form_data

        return form_data


class FormEditaValeEntregue(forms.ModelForm):
    user = forms.DateTimeField(label='Entregue por')
    user_to = forms.DateTimeField(label='Entregue para')
    vale = forms.IntegerField()
    data = forms.DateTimeField()

    class Meta:
        model = EntregaVale
        fields = ('valor', 'combustivel', 'posto', 'observacao')
        fields_order = ['vale', 'data', 'valor', 'combustivel', 'posto', 'observacao']

    def __init__(self, *args, **kwargs):
        super(FormEditaValeEntregue, self).__init__(*args, **kwargs)

        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['vale'].required = False
            self.fields['vale'].widget.attrs['disabled'] = 'disabled'
            self.fields['vale'].initial = instance.vale

            self.fields['data'].required = False
            self.fields['data'].widget.attrs['disabled'] = 'disabled'
            self.fields['data'].initial = instance.data

            self.fields['user'].required = False
            self.fields['user'].widget.attrs['disabled'] = 'disabled'
            self.fields['user'].initial = instance.user.get_full_name().title()

            self.fields['user_to'].required = False
            self.fields['user_to'].widget.attrs['disabled'] = 'disabled'
            self.fields['user_to'].initial = instance.user_to.get_full_name().title()

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})


class FormRetiraTalao(forms.Form):

    talao = forms.IntegerField(
        required=True,
        widget=forms.NumberInput({'placeholder': 'código do talão a ser devolvido'})
    )

    def __init__(self, *args, **kwargs):
        super(FormRetiraTalao, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        form_data = super(FormRetiraTalao, self).clean()
        talao_id = form_data['talao']

        if not Talao.objects.filter(talao=talao_id).exists():
            self.errors['talao'] = ['Talão NÃO encontrado']

            return form_data

        talao = Talao.objects.get(talao=talao_id)

        if talao.status != 1:
            self.errors['talao'] = ['Talão NÃO está em uso']

            return form_data

        if EntregaVale.objects.filter(vale__talao=talao).exists():
            self.errors['talao'] = [
                'Já foi entregue um ou mais vales deste talão',
                'Talão não pode ser devolvido',
            ]

        form_data['talao'] = talao

        return form_data
