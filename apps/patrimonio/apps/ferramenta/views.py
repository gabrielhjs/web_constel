from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *


@login_required()
def view_cadastrar_ferramenta(request):

    if request.method == 'POST':
        form = FormCadastraFerramenta(request.POST)

        if form.is_valid():
            ferramenta = Ferramenta(
                nome=form.cleaned_data['nome'],
                descricao=form.cleaned_data['descricao'],
                user=request.user,
            )
            ferramenta.save()
            FerramentaQuantidade(
                ferramenta=ferramenta,
                quantidade=0,
            ).save()

            return HttpResponseRedirect('/patrimonio/menu-cadastros/')
    else:
        form = FormCadastraFerramenta()

    context = {
        'ferramentas': Ferramenta.objects.all(),
        'form': form,
    }

    return render(request, 'ferramenta/cadastrar_ferramenta.html', context)


@login_required()
def view_entrada_ferramenta(request):

    if request.method == 'POST':
        form = FormEntradaFerramenta(request.POST)

        if form.is_valid():
            FerramentaEntrada(
                ferramenta=form.cleaned_data['ferramenta'],
                quantidade=form.cleaned_data['quantidade'],
                valor=form.cleaned_data['valor'],
                observacao=form.cleaned_data['observacao'],
                user=request.user,
            ).save()
            ferramenta = form.cleaned_data['ferramenta']
            ferramenta.quantidade.quantidade += form.cleaned_data['quantidade']
            ferramenta.quantidade.save()

            return HttpResponseRedirect('/patrimonio/menu-entradas/')

    else:
        form = FormEntradaFerramenta()

    return render(request, 'patrimonio/entrada.html', {'form': form})


def view_consulta_ferramentas(request):

    context = {
        'ferramentas': Ferramenta.objects.all()
    }

    return render(request, 'ferramenta/consulta_ferramenta.html', context=context)


@login_required()
def view_consulta_ferramentas_estoque(request):

    context = {
        'ferramentas': FerramentaQuantidade.objects.all()
    }

    return render(request, 'ferramenta/consulta_ferramenta_estoque.html', context=context)
