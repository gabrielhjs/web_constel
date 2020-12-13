from django import forms

from ..ferramenta.models import FerramentaSaida, Ferramenta, FerramentaQuantidade
from ..patrimonio1.models import PatrimonioId

from .models import ItemFerramenta, ItemPatrimonio


class FormInsereFerramenta(forms.ModelForm):
  class Meta:
    model = FerramentaSaida
    fields = ('ferramenta', 'quantidade')

  def __init__(self, user_to, *args, **kwargs):
    super(FormInsereFerramenta, self).__init__(*args, **kwargs)
    self.user_to = user_to

    self.fields['ferramenta'].queryset = Ferramenta.objects.filter(
      quantidade__quantidade__gt=0
    ).order_by('nome')

    for key in self.fields.keys():
      self.fields[key].widget.attrs.update({'class': 'form-control'})

  def clean(self):
    form_data = super(FormInsereFerramenta, self).clean()

    print(form_data)

    estoque = FerramentaQuantidade.objects.get(ferramenta=form_data['ferramenta']).quantidade

    if ItemFerramenta.objects.filter(
      lista__user_to__id=self.user_to,
      ferramenta=form_data['ferramenta']
    ).exists():

      lista = ItemFerramenta.objects.get(
        lista__user_to__id=self.user_to,
        ferramenta=form_data['ferramenta'],
      ).quantidade

    else:
      lista = 0

    retirada = form_data['quantidade']

    if (estoque - retirada - lista) < 0:
      self._errors['quantidade'] = ['Não há quantidade disponível em estoque! estoque: (%d)' % estoque]

    return form_data


class FormInserePatrimonio(forms.Form):

  patrimonio = forms.CharField()

  def __init__(self, user_to, *args, **kwargs):
    super(FormInserePatrimonio, self).__init__(*args, **kwargs)
    self.user_to = user_to

    for key in self.fields.keys():
      self.fields[key].widget.attrs.update({'class': 'form-control'})

  def clean(self):
    form_data = super(FormInserePatrimonio, self).clean()

    if PatrimonioId.objects.filter(codigo=int(form_data.get('patrimonio', ""))).exists:
      patrimonio = PatrimonioId.objects.get(codigo=int(form_data['patrimonio']))

    else:
      self._errors["patrimonio"] = ["Código de patrimônio não cadastrado no sistema"]
      return form_data

    if not ItemPatrimonio.objects.filter(
      lista__user_to__username=self.user_to,
      patrimonio__codigo=form_data['patrimonio']
    ).exists() and patrimonio.status != 0:
        self._errors["patrimonio"] = ["Este patrímonio não se encontra em estoque"]
        return form_data

    form_data['patrimonio'] = patrimonio

    return form_data
