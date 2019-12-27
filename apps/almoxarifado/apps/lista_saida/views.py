from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *
from apps.almoxarifado.models import MaterialSaida, Ordem


@login_required()
def view_lista_cria(request):

    if request.method == 'POST':
        form = FormListaCria(request.POST)

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
                '/almoxarifado/menu-saidas/lista/itens/' + str(form.cleaned_data['user_to']) + '/'
            )

    else:
        form = FormListaCria()

    context = {
        'form': form,
        'pagina_titulo': 'Almoxarifado',
        'menu_titulo': 'Entrega de materiais',
        'button_submit_text': 'Avançar',
    }

    return render(request, 'lista_saida/lista_cria.html', context)


@login_required()
def view_item_insere(request, user_to):

    if not Lista.objects.filter(user_to__username=user_to).exists():

        return HttpResponseRedirect('/almoxarifado/menu-saidas/lista/')

    if request.method == 'POST':
        form_insere = FormItemInsere(user_to, request.POST)

        if form_insere.is_valid():
            lista = Lista.objects.get(user_to__username=user_to)
            material = form_insere.cleaned_data['material']
            quantidade = form_insere.cleaned_data['quantidade']

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

            return HttpResponseRedirect('/almoxarifado/menu-saidas/lista/itens/' + user_to + '/')

    else:
        form_insere = FormItemInsere(user_to)

    context = {
        'lista_itens': Item.objects.filter(lista__user_to__username=user_to),
        'form': form_insere,
        'user_to': User.objects.get(username=user_to),
        'pagina_titulo': 'Almoxarifado',
        'menu_titulo': 'Entrega de materiais',
        'button_submit_text': 'Adicionar material',
    }

    return render(request, 'lista_saida/lista_itens.html', context)


@login_required()
def view_item_entrega(request, user_to):

    if not Item.objects.filter(lista__user_to__username=user_to).exists():

        return HttpResponseRedirect('/almoxarifado/menu-saidas/lista/itens/' + user_to + '/')

    else:
        itens = Item.objects.filter(lista__user_to__username=user_to)
        ordem = Ordem.objects.create(tipo=1, user=request.user)
        ordem.save()

        for item in itens:
            saida = MaterialSaida(
                material=item.material,
                quantidade=item.quantidade,
                observacao='',
                user_to=User.objects.get(username=user_to),
                user=request.user,
                ordem=ordem
            )
            material = item.material
            material.quantidade.quantidade -= item.quantidade

            material.quantidade.save()
            saida.save()

        itens[0].lista.delete()

        return HttpResponseRedirect('/almoxarifado/menu-saidas/')


def view_item_limpa(request, user_to):

    if not Lista.objects.filter(user_to__username=user_to).exists():

        return HttpResponseRedirect('/almoxarifado/menu-saidas/lista/')

    else:
        itens = Item.objects.filter(lista__user_to__username=user_to)

        for item in itens:
            item.delete()

        return HttpResponseRedirect('/almoxarifado/menu-saidas/lista/itens/' + user_to + '/')
