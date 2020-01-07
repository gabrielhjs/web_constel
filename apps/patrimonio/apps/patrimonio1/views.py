from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *
from constel.apps.controle_acessos.decorator import permission


@login_required
@permission('patrimonio', )
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
        'patrimonios': Patrimonio.objects.all().order_by('nome', 'data'),
        'form': form,
        'pagina_titulo': 'Patrimônio',
        'menu_titulo': 'Cadastro de patrimônio',
        'callback': 'patrimonio_menu_cadastros',
        'button_submit_text': 'Cadastrar patrimônio',
        'callback_text': 'Cancelar',
    }

    return render(request, 'patrimonio1/cadastrar_patrimonio.html', context)


@login_required
@permission('patrimonio', )
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

    context = {
        'form': form,
        'callback': 'patrimonio_menu_entradas',
        'button_submit_text': 'Registrar entrada',
        'callback_text': 'Cancelar',
        'pagina_titulo': 'Patrimônio',
        'menu_titulo': 'Aquisição de patrimônio',
    }

    return render(request, 'patrimonio/entrada.html', context)


@login_required
@permission('patrimonio', )
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

    context = {
        'form': form,
        'callback': 'patrimonio_menu_saidas',
        'button_submit_text': 'Registrar entrega',
        'callback_text': 'Cancelar',
        'pagina_titulo': 'Patrimônio',
        'menu_titulo': 'Entrega de patrimônio',
    }

    return render(request, 'patrimonio/entrada.html', context)


@login_required
@permission('patrimonio', )
def view_consulta_patrimonios_modelos(request):

    context = {
        'patrimonios': Patrimonio.objects.all().order_by('nome'),
        'pagina_titulo': 'Patrimônio',
        'menu_titulo': 'Patrimônios cadastrados',
    }

    return render(request, 'patrimonio1/consulta_patrimonios_modelos.html', context=context)


@login_required
@permission('patrimonio', )
def view_consulta_patrimonios(request):

    context = {
        'patrimonios': PatrimonioEntrada.objects.all().order_by('patrimonio__nome'),
        'pagina_titulo': 'Patrimônio',
        'menu_titulo': 'Patrimônio',
    }

    return render(request, 'patrimonio1/consulta_patrimonios.html', context=context)
