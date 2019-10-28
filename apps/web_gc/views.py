from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import FormTalao
from .models import Talao


def view_index(request):
    return render(request, 'web_gc/index.html')


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FormTalao(request.POST)
        # check whether it's valid:
        if form.is_valid():
            return form.save()

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
