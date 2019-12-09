from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView

from .forms import *
from .models import Ferramenta


def view_menu_principal(request):

    return render(request, 'patrimonio/menu_principal.html')


def view_menu_cadastros(request):

    return render(request, 'patrimonio/menu_cadastros.html')


def view_menu_consultas(request):

    return render(request, 'patrimonio/menu_consultas.html')


def view_menu_relatorios(request):

    return render(request, 'patrimonio/menu_relatorios.html')


def view_cadastrar_ferramenta(request):

    if request.method == 'POST':
        form = FormCadastraFerramenta(request.POST)

        if form.is_valid():
            Ferramenta(
                nome=form.cleaned_data['nome'],
                descricao=form.cleaned_data['descricao'],
                user=request.user,
            ).save()

            return HttpResponseRedirect('/patrimonio/menu-cadastros/')
    else:
        form = FormCadastraFerramenta()

    context = {
        'ferramentas': Ferramenta.objects.all(),
        'form': form,
    }

    return render(request, 'patrimonio/cadastrar_ferramenta.html', context)


class ViewConsultaFerramentas(ListView):
    model = Ferramenta
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = {
            'ferramentas': self.object_list.all(),
        }
        return context
