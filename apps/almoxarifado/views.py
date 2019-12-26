from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import Material
from constel.objects import Button


@login_required()
def view_menu_principal(request):

    button_1 = Button('almoxarifado_menu_cadastros', 'Cadastros')
    button_2 = Button('almoxarifado_menu_entradas', 'Entradas')
    button_3 = Button('almoxarifado_menu_saidas', 'Saídas')
    button_4 = Button('almoxarifado_menu_consultas', 'Consultas')
    button_5 = Button('almoxarifado_menu_relatorios', 'Relatórios')
    button_voltar = Button('index', 'Voltar')

    context = {
        'guia_titulo': 'Constel | Patrimônio',
        'pagina_titulo': 'Almoxarifado',
        'menu_titulo': 'Menu principal',
        'buttons': [
            button_1,
            button_2,
            button_3,
            button_4,
            button_5,
        ],
        'rollback': button_voltar,
    }

    return render(request, 'constel/menu.html', context)


@login_required()
def view_menu_cadastros(request):

    button_1 = Button('almoxarifado_cadastrar_material', 'Cadastrar material')
    button_2 = Button('almoxarifado_cadastrar_fornecedor', 'Cadastrar fornecedor')
    button_voltar = Button('almoxarifado_menu_principal', 'Voltar')

    context = {
        'guia_titulo': 'Constel | Patrimônio',
        'pagina_titulo': 'Almoxarifado',
        'menu_titulo': 'Menu de cadastros',
        'buttons': [
            button_1,
            button_2,
        ],
        'rollback': button_voltar,
    }

    return render(request, 'constel/menu.html', context)


@login_required()
def view_menu_entradas(request):

    button_1 = Button('almoxarifado_entrada_material', 'Aquisição de material')
    button_voltar = Button('almoxarifado_menu_principal', 'Voltar')

    context = {
        'guia_titulo': 'Constel | Patrimônio',
        'pagina_titulo': 'Almoxarifado',
        'menu_titulo': 'Menu de entradas',
        'buttons': [
            button_1,
        ],
        'rollback': button_voltar,
    }

    return render(request, 'constel/menu.html', context)


@login_required()
def view_menu_saidas(request):

    button_1 = Button('almoxarifado_saida_lista', 'Entrega de materiais')
    button_voltar = Button('almoxarifado_menu_principal', 'Voltar')

    context = {
        'guia_titulo': 'Constel | Patrimônio',
        'pagina_titulo': 'Almoxarifado',
        'menu_titulo': 'Menu de saídas',
        'buttons': [
            button_1,
        ],
        'rollback': button_voltar,
    }

    return render(request, 'constel/menu.html', context)


@login_required()
def view_menu_consultas(request):

    context = {
        'guia_titulo': 'Constel | Patrimônio',
        'pagina_titulo': 'Almoxarifado',
        'menu_titulo': 'Menu de consultas',
    }

    return render(request, 'almoxarifado/menu_consultas.html', context)


@login_required()
def view_menu_relatorios(request):

    button_voltar = Button('almoxarifado_menu_principal', 'Voltar')

    context = {
        'guia_titulo': 'Constel | Patrimônio',
        'pagina_titulo': 'Almoxarifado',
        'menu_titulo': 'Menu de relatórios',
        'buttons': [],
        'rollback': button_voltar,
    }

    return render(request, 'constel/menu.html', context)


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
            ordem = Ordem.objects.create(tipo=0, user=request.user)
            ordem.save()
            entrada = MaterialEntrada(
                material=form.cleaned_data['material'],
                quantidade=form.cleaned_data['quantidade'],
                observacao=form.cleaned_data['observacao'],
                fornecedor=form.cleaned_data['fornecedor'],
                user=request.user,
                ordem=ordem,
            )
            material = form.cleaned_data['material']
            material.quantidade.quantidade += form.cleaned_data['quantidade']

            entrada.save()
            material.quantidade.save()

            return HttpResponseRedirect('/almoxarifado/menu-entradas/')

    else:
        form = FormEntradaMaterial()

    return render(request, 'almoxarifado/entrada.html', {'form': form})


class ViewConsultaMateriais(ListView):
    model = Material
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = {
            'materiais': self.object_list.all(),
        }
        return context


def view_consulta_estoque(request):

    itens = MaterialQuantidade.objects.filter(quantidade__gt=0).order_by('material')
    context = {'itens': itens}

    return render(request, 'almoxarifado/consulta_estoque.html', context)


def view_consulta_ordem(request, tipo):

    itens = Ordem.objects.filter(tipo=tipo).order_by('data')
    context = {'itens': itens}

    return render(request, 'almoxarifado/consulta_ordem.html', context)
