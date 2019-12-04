from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView

from .forms import *
from .models import Material


def view_menu_principal(request):

    return render(request, 'almoxarifado/menu_principal.html')


def view_menu_cadastros(request):

    return render(request, 'almoxarifado/menu_cadastros.html')


def view_menu_consultas(request):

    return render(request, 'almoxarifado/menu_consultas.html')


def view_menu_relatorios(request):

    return render(request, 'almoxarifado/menu_relatorios.html')


def view_cadastrar_material(request):

    if request.method == 'POST':
        form = FormCadastraMaterial(request.POST)

        if form.is_valid():
            Material(
                codigo=form.cleaned_data['codigo'],
                material=form.cleaned_data['material'],
                descricao=form.cleaned_data['descricao'],
                user=request.user,
            ).save()

            return HttpResponseRedirect('/almoxarifado/menu-cadastros/')
    else:
        form = FormCadastraMaterial()

    context = {
        'materiais': Material.objects.all(),
        'form': form,
    }

    return render(request, 'almoxarifado/cadastrar_material.html', context)


class ViewConsultaMateriais(ListView):
    model = Material
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = {
            'materiais': self.object_list.all(),
        }
        return context
