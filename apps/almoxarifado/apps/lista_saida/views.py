from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.contrib import messages

from .models import *
from .forms import *
from apps.almoxarifado.models import MaterialSaida, Ordem
from apps.almoxarifado.apps.pdf.objects import FichaMateriais
from constel.apps.controle_acessos.decorator import permission

from ...menu import menu_principal


@login_required
@permission('almoxarifado', 'almoxarifado - saida', )
def lista_cria(request):
    menu = menu_principal(request)

    if request.method == 'POST':
        form = FormCria(request.POST)

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
                '/almoxarifado/saidas/material/lista/itens/' + str(form.cleaned_data['user_to']) + '/'
            )

    else:
        form = FormCria()

    context = {
        'form': form,
        'form_submit_text': 'Avançar',
    }
    context.update(menu)

    return render(request, 'lista_saida/v2/cria.html', context)


@login_required()
@permission('almoxarifado', 'almoxarifado - saida', )
def lista_insere(request, user_to):
    menu = menu_principal(request)

    if not Lista.objects.filter(user_to__username=user_to).exists():
        return HttpResponseRedirect('/almoxarifado/saidas/material/lista/')

    if request.method == 'POST':
        form = FormInsere(user_to, request.POST)

        if form.is_valid():
            lista = Lista.objects.get(user_to__username=user_to)
            material = form.cleaned_data['material']
            quantidade = form.cleaned_data['quantidade']

            if Item.objects.filter(lista=lista, material=material).exists():
                item = Item.objects.get(lista=lista, material=material)
                item.quantidade += quantidade

                if item.quantidade == 0:
                    item.delete()

                else:
                    item.save()

            else:
                item = Item.objects.create(lista=lista, material=material, quantidade=quantidade)
                item.save()

            return HttpResponseRedirect('/almoxarifado/saidas/material/lista/itens/' + user_to + '/')

    else:
        form = FormInsere(user_to)

    lista = Item.objects.filter(lista__user_to__username=user_to).values(
        'material__codigo',
        'material__material',
        'quantidade',
    )

    user_to = User.objects.get(username=user_to)

    context = {
        'lista_itens': lista,
        'user_to': user_to,
        'form': form,
        'form_submit_text': 'Adicionar material',
    }
    context.update(menu)

    return render(request, 'lista_saida/v2/itens.html', context)


@login_required()
@permission('almoxarifado', 'almoxarifado - saida', )
def lista_entrega(request, user_to):

    if not Item.objects.filter(lista__user_to__username=user_to).exists():
        return HttpResponseRedirect('/almoxarifado/saidas/material/lista/itens/' + user_to + '/')

    else:
        itens = Item.objects.filter(lista__user_to__username=user_to)
        ordem = Ordem.objects.create(tipo=1, user=request.user)
        ordem.save()
        user_to_object = User.objects.get(username=user_to)

        for item in itens:
            if (item.material.quantidade.quantidade - item.quantidade) < 0:
                messages.error(request, 'Não há quantidade disponível em estoque! estoque: (%d)' % item.material.quantidade)
                return HttpResponseRedirect('/almoxarifado/saidas/material/lista/itens/' + user_to + '/')

            saida = MaterialSaida(
                material=item.material,
                quantidade=item.quantidade,
                observacao='',
                user_to=user_to_object,
                user=request.user,
                ordem=ordem
            )
            material = item.material
            material.quantidade.quantidade -= item.quantidade

            material.quantidade.save()
            saida.save()

        itens[0].lista.delete()

        return HttpResponseRedirect(f'/almoxarifado/saidas/material/lista/conclui/{str(ordem.id)}')


@login_required
@permission('almoxarifado', 'almoxarifado - saida', )
def lista_conclui(request, ordem_id):
    menu = menu_principal(request)

    context = {
        'ordem_id': ordem_id,
    }
    context.update(menu)

    return render(request, 'lista_saida/v2/conclui.html', context)


@login_required
@permission('almoxarifado', 'almoxarifado - saida', )
def lista_imprime(request, ordem_id):

    if Ordem.objects.filter(id=ordem_id).exists():
        ordem = Ordem.objects.get(id=ordem_id)

    else:
        return HttpResponseRedirect('/almoxarifado/consultas/ordens/saidas/')

    ficha = FichaMateriais(ordem)

    return FileResponse(ficha.file(), filename='ficha_' + str(ordem.id) + '.pdf')


@login_required
@permission('almoxarifado', 'almoxarifado - saida', )
def lista_limpa(request, user_to):

    if not Lista.objects.filter(user_to__username=user_to).exists():
        return HttpResponseRedirect('/almoxarifado/saidas/material/lista/')

    else:
        itens = Item.objects.filter(lista__user_to__username=user_to)

        for item in itens:
            item.delete()

        return HttpResponseRedirect('/almoxarifado/saidas/material/lista/itens/' + user_to + '/')
