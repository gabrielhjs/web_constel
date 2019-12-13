from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *


@login_required()
def view_cadastrar_patrimonio(request):

    if request.method == 'POST':
        form = FormCadastraPatrimonio(request.POST)

        if form.is_valid():
            Patrimonio(
                nome=form.cleaned_data['nome'],
                descricao=form.cleaned_data['descricao'],
                user=request.user,
            ).save()

            return HttpResponseRedirect('/patrimonio/menu-cadastros/')
    else:
        form = FormCadastraPatrimonio()

    context = {
        'patrimonios': Patrimonio.objects.all(),
        'form': form,
    }

    return render(request, 'patrimonio1/cadastrar_patrimonio.html', context)


@login_required()
def view_entrada_patrimonio(request):

    if request.method == 'POST':
        form = FormEntradaPatrimonio(request.POST)

        if form.is_valid():
            PatrimonioEntrada(
                patrimonio=form.cleaned_data['patrimonio'],
                codigo=form.cleaned_data['codigo'],
                valor=form.cleaned_data['valor'],
                observacao=form.cleaned_data['observacao'],
                user=request.user,
            ).save()

            return HttpResponseRedirect('/patrimonio/menu-entradas/')

    else:
        form = FormEntradaPatrimonio()

    return render(request, 'patrimonio/entrada.html', {'form': form})


def view_consulta_patrimonio(request):

    context = {
        'patrimonios': Patrimonio.objects.all()
    }

    return render(request, 'patrimonio1/consulta_patrimonio.html', context=context)
