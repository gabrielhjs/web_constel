from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import FormTalao, FormEntregaTalao, FormEntregaVale
from .models import Talao, Vale


def view_index(request):
    return render(request, 'web_gc/index.html')


def view_cadastrar_talao(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FormTalao(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save(commit=False)
            print(form.cleaned_data['talao'])
            talao = Talao.objects.get(talao=form.cleaned_data['talao'])
            print(talao)
            for i in range(form.cleaned_data['vale_inicial'], form.cleaned_data['vale_inicial'] + 1):
                vale = Vale(vale=i, status=1, talao=talao)
                vale.save()
            form.save()
            return HttpResponseRedirect('/gc')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FormTalao()

    return render(request, 'web_gc/cadastro_talao.html', {'form': form})


def view_taloes(request):
    lista_talao = Talao.objects.all()
    context = {
        'lista_talao': lista_talao
    }
    return render(request, 'web_gc/consulta_talao.html', context)


def view_talao(request, talao_id):
    talao = Talao.objects.filter(talao=talao_id)
    context = {
        'talao': talao,
    }
    return render(request, 'web_gc/detalhes_talao.html', context)


def view_entrega_talao(request):
    if request.method == 'POST':
        form = FormEntregaTalao(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/gc')
    else:
        form = FormEntregaTalao()

    return render(request, 'web_gc/entrega_talao.html', {'form': form})


def view_entrega_vale(request):
    if request.method == 'POST':
        form = FormEntregaVale(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/gc')
    else:
        form = FormEntregaVale()

    return render(request, 'web_gc/entrega_vale.html', {'form': form})
