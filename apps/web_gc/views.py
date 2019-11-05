from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import FormTalao, FormEntregaTalao, FormEntregaVale, FormCadastraCombustivel
from .models import Talao, Vale


@login_required()
def view_index(request):
    return render(request, 'web_gc/index.html')


@login_required()
def view_cadastrar_talao(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FormTalao(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()

            talao = Talao.objects.get(talao=form.cleaned_data['talao'])

            for i in range(form.cleaned_data['vale_inicial'], form.cleaned_data['vale_final'] + 1):
                vale = Vale(vale=i, status=0, talao=talao)
                vale.save()

            return HttpResponseRedirect('/gc')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FormTalao()

    return render(request, 'web_gc/cadastro_talao.html', {'form': form})


@login_required()
def view_taloes(request):
    lista_talao = Talao.objects.all()
    context = {
        'lista_talao': lista_talao
    }
    return render(request, 'web_gc/consulta_talao.html', context)


@login_required()
def view_talao(request, talao_id):
    talao = Talao.objects.get(talao=talao_id)
    lista_vales = Vale.objects.filter(talao=talao)
    context = {
        'talao': talao,
        'lista_vales': lista_vales,
    }
    return render(request, 'web_gc/detalhes_talao.html', context)


@login_required()
def view_entrega_talao(request):
    if request.method == 'POST':
        form = FormEntregaTalao(request.POST)
        if form.is_valid():
            talao = form.cleaned_data['talao']
            talao.status = 1
            Vale.objects.filter(talao=talao).update(status=1)
            talao.save()
            form.save()
            return HttpResponseRedirect('/gc')
    else:
        form = FormEntregaTalao()

    return render(request, 'web_gc/entrega_talao.html', {'form': form})


@login_required()
def view_entrega_vale(request):
    if request.method == 'POST':
        form = FormEntregaVale(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/gc')
    else:
        form = FormEntregaVale()

    return render(request, 'web_gc/entrega_vale.html', {'form': form})


@login_required()
def view_cadastrar_combustivel(request):
    if request.method == 'POST':
        form = FormCadastraCombustivel(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/gc')
    else:
        form = FormCadastraCombustivel()

    return render(request, 'web_gc/cadastro_combustivel.html', {'form': form})
