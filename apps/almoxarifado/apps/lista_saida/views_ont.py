from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.contrib.auth.models import User
from django.contrib import messages

from .models import OntItem, OntLista
from .forms import FormListaCria, FormOntInsere
from apps.almoxarifado.models import Ordem
from apps.almoxarifado.apps.pdf.objects import FichaOnts
from constel.objects import Button
from constel.apps.controle_acessos.decorator import permission

from ..cont.models import Ont, OntEntrada, OntSaida


@login_required
@permission('almoxarifado', 'almoxarifado - saida', )
def view_lista_cria(request):

    if request.method == 'POST':
        form = FormListaCria(request.POST)

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
                '/almoxarifado/cont/menu-saidas/lista/itens/' + str(form.cleaned_data['user_to']) + '/'
            )

    else:
        form = FormListaCria()

    context = {
        'form': form,
        'pagina_titulo': 'Cont2',
        'menu_titulo': 'Entrega de Ont\'s',
        'button_submit_text': 'Avançar',
    }

    return render(request, 'lista_saida/ont_lista_cria.html', context)


@login_required()
@permission('almoxarifado', 'almoxarifado - saida', )
def view_item_insere(request, user_to):
    user_to = User.objects.get(username=user_to)

    if not OntLista.objects.filter(user_to=user_to).exists():
        return HttpResponseRedirect('/almoxarifado/cont/menu-saidas/lista/')

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

                    return HttpResponseRedirect('/almoxarifado/cont/menu-saidas/lista/itens/' + user_to.username + '/')

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

            return HttpResponseRedirect('/almoxarifado/cont/menu-saidas/lista/itens/' + user_to.username + '/')

    else:
        form_insere = FormOntInsere(user_to.username)

    carga = []

    if Ont.objects.filter(status=1).exists():
        onts = Ont.objects.filter(status=1)

        for ont in onts:
            ultima_saida = ont.saida_ont.last()

            if ultima_saida.user_to == user_to:
                carga.append(
                    {
                        'ont': ultima_saida.ont.codigo,
                        'data': ultima_saida.data,
                        'first_name': ultima_saida.user.first_name,
                        'last_name': ultima_saida.user.last_name,
                    }
                )

    funcionario = {
        'username': user_to.username,
        'first_name': user_to.first_name,
        'last_name': user_to.last_name,
    }

    context = {
        'lista_itens': OntItem.objects.filter(lista__user_to__username=user_to),
        'form': form_insere,
        'user_to': funcionario,
        'pagina_titulo': 'Cont2',
        'button_submit_text': 'Adicionar ONT',
        'menu_titulo': 'Saída de ONT\'s',
        'funcionario': funcionario,
        'carga': carga,
    }

    return render(request, 'lista_saida/ont_lista_itens.html', context)


@login_required()
@permission('almoxarifado', 'almoxarifado - saida', )
def view_item_entrega(request, user_to):

    if not OntItem.objects.filter(lista__user_to__username=user_to).exists():
        return HttpResponseRedirect('/almoxarifado/cont/menu-saidas/lista/')

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

        return HttpResponseRedirect('/almoxarifado/cont/menu-saidas/lista/itens/concluido/' + str(ordem.id) + '/')


@login_required
@permission('almoxarifado', 'almoxarifado - saida', )
def view_item_imprime(request, ordem_id):

    if Ordem.objects.filter(id=ordem_id).exists():
        ordem = Ordem.objects.get(id=ordem_id)

    else:
        return HttpResponseRedirect('/almoxarifado/cont/')

    ficha = FichaOnts(ordem)

    return FileResponse(ficha.file(), filename='ficha_' + str(ordem.id) + '.pdf')


@login_required
@permission('almoxarifado', 'almoxarifado - saida', )
def view_item_limpa(request, user_to):

    if not OntLista.objects.filter(user_to__username=user_to).exists():

        return HttpResponseRedirect('/almoxarifado/cont/menu-saidas/lista/')

    else:
        itens = OntItem.objects.filter(lista__user_to__username=user_to)

        for item in itens:
            item.delete()

        return HttpResponseRedirect('/almoxarifado/cont/menu-saidas/lista/itens/' + user_to + '/')


@login_required
@permission('almoxarifado', 'almoxarifado - saida', )
def view_item_conclui(request, ordem_id):
    button_1 = Button('almoxarifado_cont_saida_lista_itens_imprimi', 'Imprimir ficha')
    button_voltar = Button('almoxarifado_cont_saida_lista', 'Voltar')

    context = {
        'guia_titulo': 'Constel | Cont2',
        'pagina_titulo': 'Cont2',
        'menu_titulo': 'Entrega concluída!',
        'ordem_id': ordem_id,
        'button': button_1,
        'rollback': button_voltar,
    }

    return render(request, 'lista_saida/menu.html', context)
