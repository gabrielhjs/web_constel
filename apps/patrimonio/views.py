from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView

from .forms import *
from .models import Ferramenta, Patrimonio, FerramentaEntrada, FerramentaQuantidade


def view_menu_principal(request):

    return render(request, 'patrimonio/menu_principal.html')


def view_menu_cadastros(request):

    return render(request, 'patrimonio/menu_cadastros.html')


def view_menu_entradas(request):

    return render(request, 'patrimonio/menu_entradas.html')


def view_menu_consultas(request):

    return render(request, 'patrimonio/menu_consultas.html')


def view_menu_relatorios(request):

    return render(request, 'patrimonio/menu_relatorios.html')


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

    return render(request, 'patrimonio/cadastrar_ferramenta.html', context)


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

    return render(request, 'patrimonio/cadastrar_patrimonio.html', context)


class ViewConsultaFerramentas(ListView):
    model = Ferramenta
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = {
            'ferramentas': self.object_list.all(),
        }
        return context


class ViewConsultaPatrimonio(ListView):
    model = Patrimonio
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = {
            'patrimonios': self.object_list.all(),
        }
        return context


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

            return HttpResponseRedirect('/patrimonio/')

    else:
        form = FormEntradaFerramenta()

    return render(request, 'patrimonio/entrada_ferramenta.html', {'form': form})
