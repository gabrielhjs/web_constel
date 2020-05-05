from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count, Q, Max

from .models import OntItem, OntLista
from .forms import FormCria, FormOntInsere
from apps.almoxarifado.models import Ordem
from apps.almoxarifado.apps.pdf.objects import FichaOnts
from constel.objects import Button
from constel.apps.controle_acessos.decorator import permission

from ..cont.models import Ont, OntEntrada, OntSaida
from ..cont.menu import menu_principal


@login_required
@permission('almoxarifado', 'almoxarifado - saida', )
def lista_cria(request):
    menu = menu_principal(request)

    if request.method == 'POST':
        form = FormCria(request.POST)

        if form.is_valid():

            if not OntLista.objects.filter(user_to=form.cleaned_data['user_to']).exists():
                lista = OntLista.objects.create(
                    user=request.user,
                    user_to=form.cleaned_data['user_to'],
                )
                request.session.get('ont_lista_id', None)
                request.session['ont_lista_id'] = lista.id
                lista.save()

            return HttpResponseRedirect(
                '/almoxarifado/cont/saidas/lista/' + str(form.cleaned_data['user_to']) + '/'
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
def view_insere(request, user_to):
    menu = menu_principal(request)

    user_to = User.objects.get(username=user_to)

    if not OntLista.objects.filter(user_to=user_to).exists():
        return HttpResponseRedirect('/almoxarifado/cont/saidas/lista/')

    if request.method == 'POST':
        form_insere = FormOntInsere(user_to.username, request.POST)

        if form_insere.is_valid():
            lista = OntLista.objects.get(user_to=user_to)
            ont = form_insere.cleaned_data['serial']

            if ont.status == 0:
                messages.success(request, 'Ont adicionado a lista com sucesso')

            elif ont.status == 1:
                user = OntSaida.objects.filter(ont=ont).latest('data').user_to

                if user == user_to:
                    messages.error(request, 'Ont já está na carga do técnico')

                    return HttpResponseRedirect('/almoxarifado/cont/saidas/lista/' + user_to.username + '/')

                else:
                    messages.success(
                        request,
                        'Ont estava na carga de: %s, remanejada com sucesso.' % user.get_full_name().title()
                    )

            if OntItem.objects.filter(lista=lista, material=ont).exists():
                item = OntItem.objects.get(lista=lista, material=ont)
                item.delete()

            else:
                item = OntItem.objects.create(lista=lista, material=ont)
                item.save()

            return HttpResponseRedirect('/almoxarifado/cont/saidas/lista/' + user_to.username + '/')

    else:
        form_insere = FormOntInsere(user_to.username)

    sub_query = OntSaida.objects.filter(
        ont__status=1
    ).values(
        'ont__codigo',
    ).annotate(
        max_id=Max('id'),
    ).values(
        'max_id'
    )
        
    carga = OntSaida.objects.filter(
        user_to__username=user_to,
        id__in=sub_query,
    ).values(
        'ont__codigo',
    ).annotate(
        max_data=Max('data')
    ).order_by(
        '-max_data'
    )

    funcionario = {
        'username': user_to.username,
        'first_name': user_to.first_name,
        'last_name': user_to.last_name,
    }

    lista = OntItem.objects.filter(
        lista__user_to__username=user_to
    ).values(
        'material__codigo',
    )

    context = {
        'lista_itens': lista,
        'form': form_insere,
        'form_submit_text': 'Adicionar ONT',
        'user_to': funcionario,
        'carga': carga,
    }
    context.update(menu)

    return render(request, 'lista_saida/v2/itens_ont.html', context)


@login_required()
@permission('almoxarifado', 'almoxarifado - saida', )
def view_entrega(request, user_to):

    if not OntItem.objects.filter(lista__user_to__username=user_to).exists():
        return HttpResponseRedirect('/almoxarifado/cont/saidas/lista/')

    else:
        itens = OntItem.objects.filter(lista__user_to__username=user_to)
        user_to_object = User.objects.get(username=user_to)
        ordem = Ordem.objects.create(tipo=1, user=request.user)
        ordem.save()

        for item in itens:
            ont = item.material
            entrada = OntEntrada.objects.filter(ont=ont).latest('data')

            OntSaida(
                ordem=ordem,
                ont=ont,
                user=request.user,
                user_to=user_to_object,
                entrada=entrada,
            ).save()

            ont.status = 1
            ont.save()

        itens[0].lista.delete()

        return HttpResponseRedirect('/almoxarifado/cont/saidas/lista/conclui/' + str(ordem.id) + '/')


@login_required
@permission('almoxarifado', 'almoxarifado - saida', )
def view_imprime(request, ordem_id):

    if Ordem.objects.filter(id=ordem_id).exists():
        ordem = Ordem.objects.get(id=ordem_id)

    else:
        return HttpResponseRedirect('/almoxarifado/cont/')

    ficha = FichaOnts(ordem)

    return FileResponse(ficha.file(), filename='ficha_' + str(ordem.id) + '.pdf')


@login_required
@permission('almoxarifado', 'almoxarifado - saida', )
def view_limpa(request, user_to):

    if not OntLista.objects.filter(user_to__username=user_to).exists():

        return HttpResponseRedirect('/almoxarifado/cont/saidas/lista/')

    else:
        itens = OntItem.objects.filter(lista__user_to__username=user_to)

        for item in itens:
            item.delete()

        return HttpResponseRedirect('/almoxarifado/cont/saidas/lista/' + user_to + '/')


@login_required
@permission('almoxarifado', 'almoxarifado - saida', )
def view_conclui(request, ordem_id):
    menu = menu_principal(request)

    context = {
        'ordem_id': ordem_id,
    }
    context.update(menu)

    return render(request, 'lista_saida/v2/conclui_ont.html', context)
