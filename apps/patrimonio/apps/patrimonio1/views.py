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


@login_required()
def view_saida_patrimonio(request):

    if request.method == 'POST':
        form = FormSaidaPatrimonio(request.POST)

        if form.is_valid():
            entrada = form.cleaned_data['entrada']
            PatrimonioSaida(
                entrada=entrada,
                patrimonio=entrada.patrimonio,
                observacao=form.cleaned_data['observacao'],
                user=request.user,
                user_to=form.cleaned_data['user_to'],
            ).save()
            entrada.status = 1
            entrada.save()

            return HttpResponseRedirect('/patrimonio/menu-saidas/')

    else:
        form = FormSaidaPatrimonio()

    return render(request, 'patrimonio/saida.html', {'form': form})


def view_consulta_patrimonios_modelos(request):

    context = {
        'patrimonios': Patrimonio.objects.all()
    }

    return render(request, 'patrimonio1/consulta_patrimonios_modelos.html', context=context)


def view_consulta_patrimonios(request):

    context = {
        'patrimonios': PatrimonioEntrada.objects.all()
    }

    return render(request, 'patrimonio1/consulta_patrimonios.html', context=context)
