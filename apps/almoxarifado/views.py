from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Min, Max, Count, Q

import datetime

from .forms import *
from .models import Material

from constel.objects import Button
from constel.models import UserType
from constel.apps.controle_acessos.decorator import permission
from constel.forms import FormDataInicialFinalFuncionario, FormDataInicialFinal


@login_required()
@permission('almoxarifado', )
def view_menu_principal(request):

    button_1 = Button('almoxarifado_cont_menu_principal', 'Cont 2')
    button_2 = Button('almoxarifado_menu_cadastros', 'Cadastros')
    button_3 = Button('almoxarifado_menu_entradas', 'Entradas')
    button_4 = Button('almoxarifado_menu_saidas', 'Saídas')
    button_5 = Button('almoxarifado_menu_consultas', 'Consultas')
    button_6 = Button('almoxarifado_menu_relatorios', 'Relatórios')
    button_voltar = Button('index', 'Voltar')

    context = {
        'guia_titulo': 'Constel | Almoxaridado',
        'pagina_titulo': 'Almoxarifado',
        'menu_titulo': 'Menu principal',
        'buttons': [
            button_1,
            button_2,
            button_3,
            button_4,
            button_5,
            button_6,
        ],
        'rollback': button_voltar,
    }

    return render(request, 'constel/menu.html', context)


@login_required()
@permission('almoxarifado', 'gestor', )
def view_menu_cadastros(request):

    button_1 = Button('almoxarifado_cadastrar_material', 'Cadastrar material')
    button_2 = Button('almoxarifado_cadastrar_fornecedor', 'Cadastrar fornecedor')
    button_3 = Button('almoxarifado_cadastrar_usuario_passivo', 'Cadastrar técnico')
    button_voltar = Button('almoxarifado_menu_principal', 'Voltar')

    context = {
        'guia_titulo': 'Constel | Almoxaridado',
        'pagina_titulo': 'Almoxarifado',
        'menu_titulo': 'Menu de cadastros',
        'buttons': [
            button_1,
            button_2,
            button_3,
        ],
        'rollback': button_voltar,
    }

    return render(request, 'constel/menu.html', context)


@login_required()
@permission('almoxarifado', 'almoxarifado - entrada', )
def view_menu_entradas(request):

    button_1 = Button('almoxarifado_entrada_material', 'Aquisição de material')
    button_voltar = Button('almoxarifado_menu_principal', 'Voltar')

    context = {
        'guia_titulo': 'Constel | Almoxaridado',
        'pagina_titulo': 'Almoxarifado',
        'menu_titulo': 'Menu de entradas',
        'buttons': [
            button_1,
        ],
        'rollback': button_voltar,
    }

    return render(request, 'constel/menu.html', context)


@login_required()
@permission('almoxarifado', 'almoxarifado - saida', )
def view_menu_saidas(request):

    button_1 = Button('almoxarifado_saida_lista', 'Entrega de materiais')
    button_voltar = Button('almoxarifado_menu_principal', 'Voltar')

    context = {
        'guia_titulo': 'Constel | Almoxaridado',
        'pagina_titulo': 'Almoxarifado',
        'menu_titulo': 'Menu de saídas',
        'buttons': [
            button_1,
        ],
        'rollback': button_voltar,
    }

    return render(request, 'constel/menu.html', context)


@login_required()
@permission('almoxarifado', )
def view_menu_consultas(request):

    context = {
        'guia_titulo': 'Constel | Almoxaridado',
        'pagina_titulo': 'Almoxarifado',
        'menu_titulo': 'Menu de consultas',
    }

    return render(request, 'almoxarifado/menu_consultas.html', context)


@login_required()
@permission('almoxarifado', 'gestor', )
def view_menu_relatorios(request):

    button_1 = Button('almoxarifado_relatorio_tecnicos', 'Relatório de funcionários')
    button_voltar = Button('almoxarifado_menu_principal', 'Voltar')

    context = {
        'guia_titulo': 'Constel | Almoxaridado',
        'pagina_titulo': 'Almoxarifado',
        'menu_titulo': 'Menu de relatórios',
        'buttons': [
            button_1,
        ],
        'rollback': button_voltar,
    }

    return render(request, 'constel/menu.html', context)


@login_required()
@permission('almoxarifado', )
def view_cadastrar_usuario_passivo(request, callback=None):
    """
        View de cadastro de novos usuários passivos.
        :param callback: próxima página
        :param request: POST form
        :return:
        """

    if request.method == 'POST':
        form = FormCadastraUsuarioPassivo(request.POST)

        if form.is_valid():
            form.save()
            user = User.objects.get(username=form.cleaned_data['username'])
            user_type = UserType(user=user)
            user_type.save()

            if callback is not None:

                if callback == 'lista':

                    return HttpResponseRedirect('/almoxarifado/menu-saidas/lista/')

            return HttpResponseRedirect('/almoxarifado/menu-cadastros/')
    else:
        form = FormCadastraUsuarioPassivo()

    if callback is not None:
        context = {
            'form': form,
            'callback': 'almoxarifado_saida_lista',
            'button_submit_text': 'Cadastrar beneficiário',
            'callback_text': 'Cancelar',
            'pagina_titulo': 'Almoxarifado',
            'menu_titulo': 'Cadastro de técnico',
        }

    else:
        context = {
            'form': form,
            'callback': 'almoxarifado_menu_cadastros',
            'button_submit_text': 'Cadastrar beneficiário',
            'callback_text': 'Cancelar',
            'pagina_titulo': 'Almoxarifado',
            'menu_titulo': 'Cadastro de técnico',
        }

    return render(request, 'almoxarifado/cadastra_usuario_passivo.html', context)


@login_required()
@permission('almoxarifado', 'gestor', )
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
        'button_submit_text': 'Cadastrar fornecedor',
        'callback': 'almoxarifado_menu_cadastros',
        'callback_text': 'Cancelar',
        'pagina_titulo': 'Almoxarifado',
        'menu_titulo': 'Cadastro de fornecedor',
    }

    return render(request, 'almoxarifado/cadastrar_fornecedor.html', context)


@login_required()
@permission('almoxarifado', 'gestor', )
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
        'callback': 'almoxarifado_menu_cadastros',
        'button_submit_text': 'Cadastrar material',
        'callback_text': 'Cancelar',
        'pagina_titulo': 'Almoxarifado',
        'menu_titulo': 'Cadastro de material',
    }

    return render(request, 'almoxarifado/cadastrar_material.html', context)


@login_required()
@permission('almoxarifado', 'almoxarifado - entrada', )
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

    context = {
        'form': form,
        'callback': 'almoxarifado_menu_entradas',
        'button_submit_text': 'Registrar entrada',
        'callback_text': 'Cancelar',
        'pagina_titulo': 'Almoxarifado',
        'menu_titulo': 'Entrada de material',
    }

    return render(request, 'almoxarifado/entrada.html', context)


class ViewConsultaMateriais(ListView):
    model = Material
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = {
            'materiais': self.object_list.all(),
            'pagina_titulo': 'Almoxarifado',
            'menu_titulo': 'Materiais cadastrados',
        }
        return context


@login_required()
@permission('almoxarifado', )
def view_consulta_estoque(request):

    itens = MaterialQuantidade.objects.filter(quantidade__gt=0).order_by('material')
    itens = itens.values(
        'material__codigo',
        'material__material',
        'material__descricao',
        'quantidade',
    )

    context = {
        'itens': itens,
        'pagina_titulo': 'Almoxarifado',
        'menu_titulo': 'Estoque',
    }

    return render(request, 'almoxarifado/consulta_estoque.html', context)


@login_required()
@permission('almoxarifado', )
def view_consulta_ordem(request, tipo):

    itens = Ordem.objects.filter(
        tipo=tipo
    ).order_by(
        '-data'
    ).annotate(
        user_to_first_name=Min('almoxarifado_ordem_saida__user_to__first_name'),
        user_to_last_name=Min('almoxarifado_ordem_saida__user_to__last_name'),
    )
    itens = itens.values(
        'id',
        'data',
        'user__first_name',
        'user__last_name',
        'user_to_first_name',
        'user_to_last_name',
    )
    paginator = Paginator(itens, 50)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'pagina_titulo': 'Almoxarifado',
        'menu_titulo': 'Ordens',
        'tipo': tipo,
    }

    return render(request, 'almoxarifado/consulta_ordem.html', context)


@login_required()
@permission('almoxarifado', )
def view_consulta_ordem_detalhes(request, **kwargs):

    if Ordem.objects.filter(id=kwargs.get('ordem')).exists():
        ordem = Ordem.objects.get(id=kwargs.get('ordem'))

        if kwargs.get('tipo'):
            itens = MaterialSaida.objects.filter(ordem=ordem).order_by('material__material', 'material__codigo')

        else:
            itens = MaterialEntrada.objects.filter(ordem=ordem).order_by('material__material', 'material__codigo')

        context = {
            'ordem': ordem,
            'itens': itens,
            'pagina_titulo': 'Almoxarifado',
            'menu_titulo': 'Ordem',
            'tipo': kwargs.get('tipo'),
        }

        return render(request, 'almoxarifado/consulta_ordem_detalhes.html', context)

    else:

        return HttpResponseRedirect('/almoxarifado/menu-consultas/')


@login_required()
@permission('almoxarifado', )
def view_relatorio_tecnicos(request):

    data_inicial = request.GET.get('data_inicial', '')
    data_final = request.GET.get('data_final', '')
    funcionario = request.GET.get('funcionario', '')

    form = FormDataInicialFinalFuncionario(
        initial={
            'data_inicial': data_inicial,
            'data_final': data_final,
            'funcionario': funcionario,
        }
    )

    query = Q()

    if funcionario != '':
        query = query & Q(
            Q(username__icontains=funcionario) |
            Q(first_name__icontains=funcionario) |
            Q(last_name__icontains=funcionario))

    if data_inicial != '':
        data_inicial = datetime.datetime.strptime(data_inicial, "%Y-%m-%d").date()
        query = query & Q(almoxarifado_retiradas__data__gte=data_inicial)

    if data_final != '':
        data_final = datetime.datetime.strptime(data_final, "%Y-%m-%d").date()
        query = query & Q(almoxarifado_retiradas__data__lte=data_final)

    retiradas = User.objects.filter(query).annotate(
        total=Count('almoxarifado_retiradas__ordem__id', distinct=True),
        max_data=Max('almoxarifado_retiradas__data'),
    ).order_by(
        '-total'
    )

    retiradas = retiradas.values(
        'username',
        'first_name',
        'last_name',
        'max_data',
        'total',
    ).exclude(total=0)

    context = {
        'pagina_titulo': 'Relatório de funcionários',
        'button_submit_text': 'Filtrar',
        'form': form,
        'retiradas': retiradas,
    }

    return render(request, 'almoxarifado/relatorio_tecnicos.html', context)


@login_required
@permission('almoxarifado', )
def view_relatorio_tecnicos_detalhe(request, funcionario):

    data_inicial = request.GET.get('data_inicial', '')
    data_final = request.GET.get('data_final', '')

    form = FormDataInicialFinal(
        initial={
            'data_inicial': data_inicial,
            'data_final': data_final,
        }
    )

    query = Q(almoxarifado_ordem_saida__user_to__username=funcionario)

    if data_inicial != '':
        data_inicial = datetime.datetime.strptime(data_inicial, "%Y-%m-%d").date()
        query = query & Q(data__gte=data_inicial)

    if data_final != '':
        data_final = datetime.datetime.strptime(data_final, "%Y-%m-%d").date()
        query = query & Q(data__lte=data_final)

    entregas = Ordem.objects.filter(query)

    entregas = entregas.values(
        'id',
        'data',
        'user__first_name',
        'user__last_name',
    ).annotate(
        observacao=Min('almoxarifado_ordem_saida__observacao'),
        n_materiais=Count('almoxarifado_ordem_saida__id', distinct=True),
    )

    context = {
        'pagina_titulo': 'Detalhe',
        'button_submit_text': 'Filtrar',
        'form': form,
        'entregas': entregas,
        'funcionario': funcionario,
    }

    return render(request, 'almoxarifado/relatorio_tecnicos_detalhe.html', context)


def view_relatorio_tecnicos_detalhe_ordem(request, funcionario, ordem):

    data_inicial = request.GET.get('data_inicial', '')
    data_final = request.GET.get('data_final', '')

    materiais = MaterialSaida.objects.filter(ordem=ordem)

    materiais = materiais.values(
        'ordem__id',
        'material__material',
        'quantidade',
        'data',
        'user__first_name',
        'user__last_name',
        'user_to__first_name',
        'user_to__last_name',
    )

    context = {
        'pagina_titulo': 'Detalhe ordem',
        'materiais': materiais,
        'ordem': ordem,
        'funcionario': funcionario,
    }

    return render(request, 'almoxarifado/relatorio_tecnicos_detalhe_ordem.html', context)
