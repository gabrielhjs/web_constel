from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect, FileResponse
from django.shortcuts import render

from apps.almoxarifado.apps.lista_saida.forms import FormCria
from apps.patrimonio.models import Ordem
from constel.apps.controle_acessos.decorator import permission

from ..ferramenta.models import FerramentaSaida, FerramentaQuantidadeFuncionario
from ..patrimonio1.models import PatrimonioEntrada1, PatrimonioSaida
from ..pdf.objects import FichaPatrimonio
from ...menu import menu_principal
from .models import Lista, ItemFerramenta, ItemPatrimonio
from .forms import FormInsereFerramenta, FormInserePatrimonio


@login_required
@permission('patrimonio', )
def lista_cria(request):
  menu = menu_principal(request)
  form = FormCria(request.POST or None)

  if request.method == 'POST':
    if form.is_valid():

      if not Lista.objects.filter(user_to=form.cleaned_data['user_to']).exists():
        lista = Lista.objects.create(
          user=request.user,
          user_to=form.cleaned_data['user_to'],
        )
        request.session.get('lista_id', None)
        request.session['lista_id'] = lista.id
        lista.save()

      return HttpResponseRedirect(
        '/patrimonio/saidas/lista/itens/' + str(form.cleaned_data['user_to'].id) + '/'
      )

  context = {
    'form': form,
    'form_submit_text': 'Avançar',
  }
  context.update(menu)

  return render(request, 'lista_saida/v2/cria.html', context)


@login_required()
@permission('patrimonio', )
def lista_insere(request, user_to):
  menu = menu_principal(request)

  if not Lista.objects.filter(user_to__id=user_to).exists():
    return HttpResponseRedirect('/patrimonio/saidas/lista/')

  form_ferramenta = FormInsereFerramenta(user_to)
  form_patrimonio = FormInserePatrimonio(user_to)

  if ItemFerramenta.objects.filter(lista__user_to__id=user_to).exists():
    lista_ferramenta = ItemFerramenta.objects.filter(lista__user_to__id=user_to).values(
      'ferramenta__nome',
      'quantidade',
    )

  else:
    lista_ferramenta = []

  if ItemPatrimonio.objects.filter(lista__user_to__id=user_to).exists():
    lista_patrimonio = ItemPatrimonio.objects.filter(lista__user_to__id=user_to).values(
      'patrimonio__codigo',
      'patrimonio__patrimonio__nome',
    )

  else:
    lista_patrimonio = []

  user_to = User.objects.get(id=user_to)

  context = {
    'user_to': user_to,
    'lista_ferramenta': lista_ferramenta,
    'lista_patrimonio': lista_patrimonio,
    'form_ferramenta': form_ferramenta,
    'form_patrimonio': form_patrimonio,
    'form_submit_ferramenta_text': 'adicionar ferramenta',
    'form_submit_patrimonio_text': 'adicionar patrimônio',
  }
  context.update(menu)

  return render(request, 'lista_saida_patrimonio/v2/itens.html', context)


@login_required()
@permission('patrimonio', )
def lista_insere_ferramenta(request, user_to):

  if request.method == 'POST':
    form_ferramenta = FormInsereFerramenta(user_to=user_to, data=request.POST)
    lista, created = Lista.objects.get_or_create(user_to__id=user_to)

    if form_ferramenta.is_valid():
      ferramenta = form_ferramenta.cleaned_data['ferramenta']
      quantidade = form_ferramenta.cleaned_data['quantidade']

      if ItemFerramenta.objects.filter(lista=lista, ferramenta=ferramenta).exists():
        item = ItemFerramenta.objects.get(lista=lista, ferramenta=ferramenta)
        item.quantidade += quantidade

        if item.quantidade == 0:
          item.delete()

        else:
          item.save()

      else:
        item = ItemFerramenta.objects.create(lista=lista, ferramenta=ferramenta, quantidade=quantidade)
        item.save()

  return HttpResponseRedirect(f'/patrimonio/saidas/lista/itens/{user_to}/')


@login_required()
@permission('patrimonio', )
def lista_insere_patrimonio(request, user_to):
  if request.method == 'POST':
    form_patrimonio = FormInserePatrimonio(user_to, data=request.POST)
    lista, created = Lista.objects.get_or_create(user_to__id=user_to)

    if form_patrimonio.is_valid():
      patrimonio = form_patrimonio.cleaned_data["patrimonio"]

      if ItemPatrimonio.objects.filter(lista__user_to__id=user_to, patrimonio=patrimonio).exists():
        item = ItemPatrimonio.objects.get(lista__user_to__id=user_to, patrimonio=patrimonio)
        item.delete()
        messages.success(request, 'Patrimônio retirado da lista com sucesso')

      else:
        item = ItemPatrimonio.objects.create(lista=lista, patrimonio=patrimonio)
        item.save()

  return HttpResponseRedirect(f'/patrimonio/saidas/lista/itens/{user_to}/')


@login_required
@permission('patrimonio', )
def lista_entrega(request, user_to):
  if (
    not ItemFerramenta.objects.filter(lista__user_to__id=user_to).exists() and
    not ItemPatrimonio.objects.filter(lista__user_to__id=user_to).exists()
  ):
    return HttpResponseRedirect(f'/patrimonio/saidas/lista/itens/{user_to}/')

  else:
    ordem = Ordem.objects.create(tipo=1, user=request.user)
    ordem.save()

    user_to_object = User.objects.get(id=user_to)

    if ItemFerramenta.objects.filter(lista__user_to__id=user_to).exists():
      itens_ferramenta = ItemFerramenta.objects.filter(lista__user_to__id=user_to)

      for item in itens_ferramenta:
        if (item.ferramenta.quantidade.quantidade - item.quantidade) < 0:
          messages.error(
            request,
            'Não há quantidade disponível em estoque! estoque: (%d)' % item.ferramenta.quantidade.quantidade
          )
          return HttpResponseRedirect(f'/patrimonio/saidas/lista/itens/{user_to}/')

        saida = FerramentaSaida(
          ferramenta=item.ferramenta,
          quantidade=item.quantidade,
          user_to=user_to_object,
          user=request.user,
          ordem=ordem,
        )

        item.ferramenta.quantidade.quantidade -= item.quantidade

        if FerramentaQuantidadeFuncionario.objects.filter(
          user=user_to_object,
          ferramenta=item.ferramenta
        ).exists():

          carga = FerramentaQuantidadeFuncionario.objects.get(
            user=user_to_object,
            ferramenta=item.ferramenta
          )
          carga.quantidade += item.quantidade

        else:
          carga = FerramentaQuantidadeFuncionario(
            user=user_to_object,
            ferramenta=item.ferramenta,
            quantidade=item.quantidade
          )

        item.ferramenta.quantidade.save()
        saida.save()
        carga.save()

    if ItemPatrimonio.objects.filter(lista__user_to__id=user_to).exists():
      itens_patrimonio = ItemPatrimonio.objects.filter(lista__user_to__id=user_to)

      for item in itens_patrimonio:
        entrada = PatrimonioEntrada1.objects.filter(
          patrimonio=item.patrimonio,
        ).last()

        patrimonio_saida = PatrimonioSaida(
          entrada=entrada,
          patrimonio=item.patrimonio,
          user=request.user,
          user_to=user_to_object,
          ordem=ordem,
        )

        patrimonio_saida.save()
        item.patrimonio.status = 1
        item.patrimonio.save()

    if Lista.objects.filter(user_to__id=user_to).exists():
      Lista.objects.get(user_to__id=user_to).delete()

    return HttpResponseRedirect(f'/patrimonio/saidas/lista/conclui/{ordem.id}')


@login_required
@permission('patrimonio', )
def lista_conclui(request, ordem_id):
    menu = menu_principal(request)

    context = {
        'ordem_id': ordem_id,
    }
    context.update(menu)

    return render(request, 'lista_saida_patrimonio/v2/conclui.html', context)


@login_required
@permission('patrimonio', )
def lista_imprime(request, ordem_id):
    if not Ordem.objects.filter(id=ordem_id).exists():
        return HttpResponseRedirect('/patrimonio/consultas/ordens/saidas/')

    ficha = FichaPatrimonio(ordem_id)

    return FileResponse(ficha.file(), filename=f'ficha_{ordem_id}.pdf')


@login_required
@permission('patrimonio', )
def lista_limpa(request, user_to):
  if not Lista.objects.filter(user_to__id=user_to).exists():
    return HttpResponseRedirect('/patrimonio/saidas/lista/')

  else:
    itens_ferramenta = ItemFerramenta.objects.filter(lista__user_to__id=user_to)
    itens_patrimonio = ItemPatrimonio.objects.filter(lista__user_to__id=user_to)

    for item in itens_ferramenta:
      item.delete()

    for item in itens_patrimonio:
      item.delete()

    return HttpResponseRedirect(f'/patrimonio/saidas/lista/itens/{user_to}/')


@login_required
@permission('patrimonio', )
def lista_limpa_ferramenta(request, user_to):
  if not Lista.objects.filter(user_to__id=user_to).exists():
    return HttpResponseRedirect('/patrimonio/saidas/lista/')

  else:
    itens_ferramenta = ItemFerramenta.objects.filter(lista__user_to__id=user_to)

    for item in itens_ferramenta:
      item.delete()

    return HttpResponseRedirect(f'/patrimonio/saidas/lista/itens/{user_to}/')


@login_required
@permission('patrimonio', )
def lista_limpa_patrimonio(request, user_to):
  if not Lista.objects.filter(user_to__id=user_to).exists():
    return HttpResponseRedirect('/patrimonio/saidas/lista/')

  else:
    itens_patrimonio = ItemPatrimonio.objects.filter(lista__user_to__id=user_to)

    for item in itens_patrimonio:
      item.delete()

    return HttpResponseRedirect(f'/patrimonio/saidas/lista/itens/{user_to}/')
