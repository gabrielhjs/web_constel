from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import Material


@login_required()
def view_menu_principal(request):

    return render(request, 'almoxarifado/menu_principal.html')


@login_required()
def view_menu_cadastros(request):

    return render(request, 'almoxarifado/menu_cadastros.html')


@login_required()
def view_menu_entradas(request):

    return render(request, 'almoxarifado/menu_entradas.html')


@login_required()
def view_menu_saidas(request):

    return render(request, 'almoxarifado/menu_saidas.html')


@login_required()
def view_menu_consultas(request):

    return render(request, 'almoxarifado/menu_consultas.html')


@login_required()
def view_menu_relatorios(request):

    return render(request, 'almoxarifado/menu_relatorios.html')


@login_required()
def view_cadastrar_fornecedor(request):

    if request.method == 'POST':
        form = FormCadastraFornecedor(request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/almoxarifado/menu-cadastros/')
    else:
        form = FormCadastraFornecedor()

    context = {
        'fornecedores': Fornecedor.objects.all().order_by('nome', 'cnpj'),
        'form': form,
    }

    return render(request, 'almoxarifado/cadastrar_fornecedor.html', context)


@login_required()
def view_cadastrar_material(request):

    if request.method == 'POST':
        form = FormCadastraMaterial(request.POST)

        if form.is_valid():
            material = Material(
                codigo=form.cleaned_data['codigo'],
                material=form.cleaned_data['material'],
                descricao=form.cleaned_data['descricao'],
                user=request.user,
            )
            material.save()
            MaterialQuantidade(
                material=material,
                quantidade=0,
            ).save()

            return HttpResponseRedirect('/almoxarifado/menu-cadastros/')
    else:
        form = FormCadastraMaterial()

    context = {
        'materiais': Material.objects.all(),
        'form': form,
    }

    return render(request, 'almoxarifado/cadastrar_material.html', context)


@login_required()
def view_entrada_material(request):

    if request.method == 'POST':
        form = FormEntradaMaterial(request.POST)

        if form.is_valid():
            entrada = MaterialEntrada(
                material=form.cleaned_data['material'],
                quantidade=form.cleaned_data['quantidade'],
                observacao=form.cleaned_data['observacao'],
                fornecedor=form.cleaned_data['fornecedor'],
                user=request.user,
            )
            material = form.cleaned_data['material']
            material.quantidade.quantidade += form.cleaned_data['quantidade']

            entrada.save()
            material.quantidade.save()

            return HttpResponseRedirect('/almoxarifado/menu-entradas/')

    else:
        form = FormEntradaMaterial()

    return render(request, 'almoxarifado/entrada.html', {'form': form})


@login_required()
def view_saida_material_individual(request):

    if request.method == 'POST':
        form = FormSaidaMaterial(request.POST)

        if form.is_valid():
            saida = MaterialSaida(
                material=form.cleaned_data['material'],
                quantidade=form.cleaned_data['quantidade'],
                observacao=form.cleaned_data['observacao'],
                user_to=form.cleaned_data['user_to'],
                user=request.user,
            )
            material = form.cleaned_data['material']
            material.quantidade.quantidade -= form.cleaned_data['quantidade']

            material.quantidade.save()
            saida.save()

            return HttpResponseRedirect('/almoxarifado/menu-saidas/')

    else:
        form = FormSaidaMaterial()

    return render(request, 'almoxarifado/saida.html', {'form': form})


@login_required()
def view_saida_materiais1(request):

    if request.method == 'POST':
        initial = {
            'user_to': request.session.get('almoxarifado_user_to', None),
            'materiais': request.session.get('materiais', None),
        }

        form = FormSaidaMateriais1(request.POST, initial=initial)

        if form.is_valid():
            request.session['almoxarifado_user_to'] = form.cleaned_data['user_to'].id
            request.session['materiais'] = []

            return HttpResponseRedirect('/almoxarifado/menu-saidas/materiais/2/')

    else:
        form = FormSaidaMateriais1()

    return render(request, 'almoxarifado/saida.html', {'form': form})


@login_required()
def view_saida_materiais2(request):

    if request.session.get('almoxarifado_user_to') is None:
        return HttpResponseRedirect('/almoxarifado/menu-saidas/materiais/1/')

    if request.method == 'POST':
        form = FormSaidaMateriais2(request.POST)

        if form.is_valid():
            request.session['materiais'].append(
                [
                    form.cleaned_data['material'],
                    form.cleaned_data['quantidade'],
                    form.cleaned_data['observacao'],
                ]
            )
            print('Deu certo')
            print(request.session['materiais'])

            return HttpResponseRedirect('/almoxarifado/menu-saidas/materiais/2/')

    else:
        form = FormSaidaMateriais2()

    context = {
        'form': form,
        'materiais': request.session['materiais']
    }

    return render(request, 'almoxarifado/saida.html', context)


class ViewConsultaMateriais(ListView):
    model = Material
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = {
            'materiais': self.object_list.all(),
        }
        return context
