from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.contrib import messages

from .models import ManutencaoOntLista, ManutencaoOntItem
from .forms import FormOntDefeitoFornecedor, FormOntInsere
from apps.almoxarifado.models import Ordem, Fornecedor
from apps.almoxarifado.apps.pdf.objects import FichaOntsManutencao
from constel.apps.controle_acessos.decorator import permission

from ..cont.menu import menu_fechamento
from ..cont.models import OntFechamento, OntDevolucao


@login_required
@permission('almoxarifado', 'almoxarifado - saida', )
def lista_cria(request):
    menu = menu_fechamento(request)

    if request.method == 'POST':
        form = FormOntDefeitoFornecedor(request.POST)

        if form.is_valid():
            fornecedor = form.cleaned_data['fornecedor']

            if not ManutencaoOntLista.objects.filter(fornecedor=fornecedor).exists():
                lista = ManutencaoOntLista.objects.create(
                    user=request.user,
                    fornecedor=fornecedor,
                )
                request.session.get('ont_manutencao_lista_id', None)
                request.session['ont_manutencao_lista_id'] = lista.id
                lista.save()

            return HttpResponseRedirect(
                '/almoxarifado/cont/manutencao/saidas/lista/' + str(fornecedor.id) + '/'
            )

    else:
        form = FormOntDefeitoFornecedor()

    context = {
        'form': form,
        'form_submit_text': 'Avançar',
    }
    context.update(menu)

    return render(request, 'lista_saida/v2/cria.html', context)


@login_required()
@permission('almoxarifado', 'almoxarifado - saida', )
def view_insere(request, fornecedor):
    menu = menu_fechamento(request)

    fornecedor = Fornecedor.objects.get(id=fornecedor)

    if not ManutencaoOntLista.objects.filter(fornecedor=fornecedor).exists():
        return HttpResponseRedirect('/almoxarifado/cont/manutencao/saidas/lista/')

    if request.method == 'POST':
        form_insere = FormOntInsere(fornecedor.id, request.POST)

        if form_insere.is_valid():
            lista = ManutencaoOntLista.objects.get(fornecedor=fornecedor)
            ont = form_insere.cleaned_data['serial']

            if ont.status != 5:
                messages.error(request, 'Ont não consta como retirada de manutenção')

            elif ManutencaoOntItem.objects.filter(lista=lista, material=ont).exists():
                item = ManutencaoOntItem.objects.get(lista=lista, material=ont)
                item.delete()
                messages.success(request, 'Ont retirada da lista com sucesso')

            else:
                item = ManutencaoOntItem.objects.create(lista=lista, material=ont)
                item.save()
                messages.success(request, 'Ont adicionada à lista com sucesso')

            return HttpResponseRedirect('/almoxarifado/cont/manutencao/saidas/lista/' + str(fornecedor.id))

    else:
        form_insere = FormOntInsere(fornecedor)

    fornecedor_dados = {
        'nome': fornecedor.nome,
        'cnpj': fornecedor.cnpj,
        'id': fornecedor.id,
    }

    lista = ManutencaoOntItem.objects.filter(
        lista__fornecedor=fornecedor
    ).values(
        'material__codigo',
        'material__modelo__nome',
        'material__secao__nome',
    )

    context = {
        'lista_itens': lista,
        'form': form_insere,
        'form_submit_text': 'Adicionar ONT',
        'fornecedor': fornecedor_dados,
    }
    context.update(menu)

    return render(request, 'lista_saida/v2/itens_ont_manutencao.html', context)


@login_required()
@permission('almoxarifado', 'almoxarifado - saida', )
def view_entrega(request, fornecedor):

    fornecedor = Fornecedor.objects.get(id=fornecedor)

    if not ManutencaoOntItem.objects.filter(lista__fornecedor=fornecedor).exists():
        return HttpResponseRedirect('/almoxarifado/cont/manutencao/saidas/lista/')

    else:
        itens = ManutencaoOntItem.objects.filter(lista__fornecedor=fornecedor)
        ordem = Ordem.objects.create(tipo=1, user=request.user)
        ordem.save()

        for item in itens:
            ont = item.material
            fechamento = OntFechamento.objects.filter(ont=ont).latest('data')

            OntDevolucao(
                ordem=ordem,
                ont=ont,
                user=request.user,
                fornecedor=fornecedor,
                fechamento=fechamento,
            ).save()

            ont.status = 4
            ont.save()

        itens[0].lista.delete()

        return HttpResponseRedirect('/almoxarifado/cont/manutencao/saidas/conclui/' + str(ordem.id))


@login_required
@permission('almoxarifado', 'almoxarifado - saida', )
def view_imprime(request, ordem_id):

    if Ordem.objects.filter(id=ordem_id).exists():
        ordem = Ordem.objects.get(id=ordem_id)

    else:
        return HttpResponseRedirect('/almoxarifado/cont/manutencao')

    ficha = FichaOntsManutencao(ordem)

    return FileResponse(ficha.file(), filename='ficha_' + str(ordem.id) + '.pdf')


@login_required
@permission('almoxarifado', 'almoxarifado - saida', )
def view_limpa(request, fornecedor):

    fornecedor = Fornecedor.objects.get(id=fornecedor)

    if not ManutencaoOntLista.objects.filter(forneedor=fornecedor).exists():
        return HttpResponseRedirect('/almoxarifado/cont/saidas/lista/')

    else:
        itens = ManutencaoOntLista.objects.filter(lista__fornecedor=fornecedor)

        for item in itens:
            item.delete()

        return HttpResponseRedirect('/almoxarifado/cont/manutencao/saidas/lista/' + str(fornecedor.id))


@login_required
@permission('almoxarifado', 'almoxarifado - saida', )
def view_conclui(request, ordem_id):
    menu = menu_fechamento(request)

    context = {
        'ordem_id': ordem_id,
    }
    context.update(menu)

    return render(request, 'lista_saida/v2/conclui_ont_manutencao.html', context)
