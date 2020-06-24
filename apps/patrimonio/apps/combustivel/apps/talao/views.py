from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db.models import Sum, Max, Count, Q, F
from django.core.paginator import Paginator

import datetime

from .forms import *
from .models import Talao, Vale, CadastroTalao, EntregaTalao, EntregaVale, Combustivel
from .menu import menu_principal, menu_consultas, menu_cadastros, menu_taloes, menu_vales, menu_relatorios
from constel.apps.controle_acessos.decorator import permission
from constel.forms import FormDataInicialFinal, FormDataInicialFinalFuncionario, FormFiltraQ


@login_required()
@permission('patrimonio', )
def index(request):
    context = menu_principal(request)

    return render(request, 'constel/v2/app.html', context)


@login_required()
@permission('patrimonio', )
def cadastros(request):
    context = menu_cadastros(request)

    return render(request, 'constel/v2/app.html', context)


@login_required()
@permission('patrimonio', 'patrimonio - combustivel', 'patrimonio - combustivel - talao', )
def cadastrar_combustivel(request):
    """
    View de carregamento e gestão de combustível novos cadastrados no sistema,
    deve ser acessado apenas pelo adm e funcionãrios autorizados
    :param request: informações do formulário
    :return: carregamento do formulário
    """
    menu = menu_cadastros(request)

    if request.method == 'POST':
        # Registro do cadastro do combustível
        form = FormCadastraCombustivel(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/patrimonio/combustivel/talao/cadastros/combustivel')
    else:
        form = FormCadastraCombustivel()

    itens = Combustivel.objects.all().values(
        'combustivel'
    )

    paginator = Paginator(itens, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form': form,
        'form_submit_text': 'Cadastrar combustível',
    }
    context.update(menu)

    return render(request, 'talao/v2/cadastrar_combustivel.html', context)


@login_required()
@permission('patrimonio', 'patrimonio - combustivel', 'patrimonio - combustivel - talao', )
def cadastrar_posto(request):
    """
    View de carregamento e gestão de combustível novos cadastrados no sistema,
    deve ser acessado apenas pelo adm e funcionãrios autorizados
    :param request: informações do formulário
    :return: carregamento do formulário
    """
    menu = menu_cadastros(request)

    if request.method == 'POST':
        # Registro do cadastro do posto
        form = FormCadastraPosto(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/patrimonio/combustivel/talao/cadastros/posto')
    else:
        form = FormCadastraPosto()

    itens = Posto.objects.all().values(
        'posto',
    )

    paginator = Paginator(itens, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form': form,
        'form_submit_text': 'Cadastrar posto',
    }
    context.update(menu)

    return render(request, 'talao/v2/cadastrar_posto.html', context)


@login_required()
@permission('patrimonio - combustivel', 'patrimonio - combustivel - talao', )
def cadastrar_talao(request):
    """
    View de carregamento e gestão do cadastro de novos talões,
    Deve ser acessada somente pelo adm e funcionários autorizados
    :param request: informações do formulário
    :return: carregamento do formulário
    """
    menu = menu_cadastros(request)

    if request.method == 'POST':
        form = FormCadastraTalao(request.POST)

        if form.is_valid():
            # Registro do cadastro do novo talão
            talao = Talao.objects.create(talao=form.cleaned_data['talao'])
            talao.save()
            cadastro_talao = CadastroTalao(talao=talao, user=request.user)

            for i in range(form.cleaned_data['vale_inicial'], form.cleaned_data['vale_final'] + 1):
                vale = Vale.objects.create(vale=i, talao=talao)
                vale.save()

            cadastro_talao.save()
            return HttpResponseRedirect('/patrimonio/combustivel/talao/cadastros/talao')

    else:
        form = FormCadastraTalao()

    context = {
        'form': form,
        'form_submit_text': 'Cadastrar talão',
    }
    context.update(menu)

    return render(request, 'talao/v2/cadastrar_talao.html', context)


@login_required()
@permission('patrimonio - combustivel', 'patrimonio - combustivel - talao', )
def taloes(request):
    context = menu_taloes(request)

    return render(request, 'constel/v2/app.html', context)


@login_required()
@permission('patrimonio - combustivel', 'patrimonio - combustivel - talao', )
def entregar_talao(request):
    """
    View de carregamento e gestão de entrega de talões cadastrados no sistema,
    deve ser acessado apenas pelo adm e funcionãrios autorizados
    :param request: informações do formulário
    :return: carregamento do formulário
    """
    menu = menu_taloes(request)

    if request.method == 'POST':
        # Registro da entrega do talão
        form = FormEntregaTalao(request.POST)

        if form.is_valid():
            talao = form.cleaned_data['talao']
            talao.status = 1
            Vale.objects.filter(talao=talao).update(status=1)
            entrega_talao = EntregaTalao(
                talao=talao,
                user=request.user,
                user_to=form.cleaned_data['user_to'],
            )
            entrega_talao.save()
            talao.save()
            return HttpResponseRedirect('/patrimonio/combustivel/talao/taloes')
    else:
        form = FormEntregaTalao()

    context = {
        'form': form,
        'form_submit_text': 'Entregar talão',
    }
    context.update(menu)

    return render(request, 'talao/v2/entregar_talao.html', context)


@login_required()
@permission('patrimonio',)
def vales(request):
    context = menu_vales(request)

    return render(request, 'constel/v2/app.html', context)


@login_required()
@permission('patrimonio - combustivel - vale',)
def entregar_vale_1(request):
    """
    View 1 de carregamento e gestão de entrega de vales cadastrados no sistema,
    deve ser acessado apenas pelo adm e funcionãrios autorizados
    :param request: informações do formulário
    :return: carregamento do formulário
    """
    menu = menu_vales(request)

    if request.method == 'POST':
        initial = {
            'user_to': request.session.get('user_to', None),
            'vale': request.session.get('vale', None),
        }
        form = FormEntregaVale1(data=request.POST, user=request.user, initial=initial)

        if form.is_valid():
            # Registro da entrega do vale
            request.session['user_to'] = form.cleaned_data['user_to']
            request.session['vale'] = form.cleaned_data['vale']

            return HttpResponseRedirect('/patrimonio/combustivel/talao/vales/entrega-2')

    else:
        form = FormEntregaVale1(user=request.user)

    context = {
        'form': form,
        'form_submit_text': 'Avançar',
    }
    context.update(menu)

    return render(request, 'talao/v2/entregar_vale.html', context)


@login_required()
@permission('patrimonio - combustivel - vale',)
def entregar_vale_2(request):
    """
    View 2 de carregamento e gestão de entrega de vales cadastrados no sistema,
    deve ser acessado apenas pelo adm e funcionãrios autorizados
    :param request: informações do formulário
    :return: carregamento do formulário
    """
    menu = menu_vales(request)

    if request.session.get('user_to') is None:
        return HttpResponseRedirect('/patrimonio/combustivel/talao/vales/entrega-1')

    vale = Vale.objects.get(id=request.session['vale'])
    user_to = User.objects.get(id=request.session['user_to'])

    if request.method == 'POST':
        form = FormEntregaVale2(user_to, request.POST)

        if form.is_valid():
            request.session.pop('vale')
            request.session.pop('user_to')

            vale.status = 2
            vale.save()

            EntregaVale(
                user=request.user,
                user_to=user_to,
                vale=vale,
                combustivel=form.cleaned_data['combustivel'],
                valor=form.cleaned_data['valor'],
                observacao=form.cleaned_data['observacao'],
                posto=Posto.objects.get(id=form.cleaned_data['posto']),
            ).save()

            return HttpResponseRedirect('/patrimonio/combustivel/talao/vales')

    else:
        form = FormEntregaVale2(user_to)

    context = {
        'form': form,
        'form_submit_text': 'Entregar vale',
    }
    context.update(menu)

    return render(request, 'talao/v2/entregar_vale.html', context)


@login_required()
@permission('patrimonio',)
def consultas(request):
    context = menu_consultas(request)

    return render(request, 'constel/v2/app.html', context)


@login_required()
@permission('patrimonio - combustivel - vale',)
def consulta_talao(request):
    """
    View de exibição dos talões cadastrados no sistema
    :param request: informações gerais
    :return: template
    """
    menu = menu_consultas(request)

    q = request.GET.get('q', '')

    form = FormFiltraQ(
        'código do talão ou matrícula',
        initial={
            'q': q,
        }
    )

    query = Q()

    if q != '':
        query = query & Q(
            Q(talao__icontains=q) |
            Q(talao_cadastro__user__username__icontains=q) |
            Q(talao_entrega__user__username__icontains=q) |
            Q(talao_entrega__user_to__username__icontains=q)
        )

    itens = Talao.objects.filter(query).values(
        'talao',
        'status',
        'talao_cadastro__data',
        'talao_cadastro__user__username',
        'talao_cadastro__user__first_name',
        'talao_cadastro__user__last_name',
        'talao_entrega__data',
        'talao_entrega__user__username',
        'talao_entrega__user__first_name',
        'talao_entrega__user__last_name',
        'talao_entrega__user_to__username',
        'talao_entrega__user_to__first_name',
        'talao_entrega__user_to__last_name',
    ).order_by('talao')

    paginator = Paginator(itens, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form': form,
        'form_submit_text': 'Filtrar',
    }
    context.update(menu)

    return render(request, 'talao/v2/consulta_talao.html', context)


@login_required()
@permission('patrimonio - combustivel - vale',)
def consulta_talao_detalhe(request, talao):
    """
    View de exibição dos talões cadastrados no sistema
    :param request: informações gerais
    :param talao: identificação do talao a ser detalhado
    :return: lista de vales do talão
    """
    if not Talao.objects.filter(talao=talao).exists():
        return HttpResponseRedirect('/patrimonio/combustivel/talao/consultas/talao')

    menu = menu_consultas(request)

    talao = Talao.objects.get(talao=talao)

    itens = Vale.objects.filter(talao=talao).values(
        'vale',
        'status',
        'vale_entrega__data',
        'vale_entrega__user_to__first_name',
        'vale_entrega__user_to__last_name',
        'vale_entrega__combustivel__combustivel',
        'vale_entrega__valor',
        'vale_entrega__posto__posto',
        'vale_entrega__observacao',
    ).order_by('vale_entrega__data')

    context = {
        'talao': talao,
        'itens': itens,
    }
    context.update(menu)

    return render(request, 'talao/v2/consulta_talao_detalhe.html', context)


@login_required()
@permission('patrimonio - combustivel - vale',)
def consulta_meu_talao(request):
    """
    View de exibição dos talões cadastrados no sistema que foram recebido pelo usuário logado
    :param request: informações gerais
    :return: template
    """
    menu = menu_consultas(request)

    q = request.GET.get('q', '')

    form = FormFiltraQ(
        'código do talão ou matrícula',
        initial={
            'q': q,
        }
    )

    query = Q(talao_entrega__user=request.user)

    if q != '':
        query = query & Q(
            Q(talao__icontains=q) |
            Q(talao_cadastro__user__username__icontains=q) |
            Q(talao_entrega__user__username__icontains=q) |
            Q(talao_entrega__user_to__username__icontains=q)
        )

    itens = Talao.objects.filter(query).values(
        'talao',
        'status',
        'talao_cadastro__data',
        'talao_cadastro__user__username',
        'talao_cadastro__user__first_name',
        'talao_cadastro__user__last_name',
        'talao_entrega__data',
        'talao_entrega__user__username',
        'talao_entrega__user__first_name',
        'talao_entrega__user__last_name',
        'talao_entrega__user_to__username',
        'talao_entrega__user_to__first_name',
        'talao_entrega__user_to__last_name',
    ).order_by('talao')

    paginator = Paginator(itens, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form': form,
        'form_submit_text': 'Filtrar',
    }
    context.update(menu)

    return render(request, 'talao/v2/consulta_talao.html', context)


@login_required()
@permission('patrimonio - combustivel - vale',)
def consulta_meu_vale(request):
    """
    View de exibição dos vales cadastrados no sistema que foram recebidos pelo usuário cadastrado
    :param request: informações gerais
    :return: template
    """
    menu = menu_consultas(request)

    q = request.GET.get('q', '')

    form = FormFiltraQ(
        'código do vale ou matrícula',
        initial={
            'q': q,
        }
    )

    query = Q(vale_entrega__user_to=request.user)

    if q != '':
        query = query & Q(
            Q(vale__icontains=q) |
            Q(vale_entrega__user__username__icontains=q)
        )

    itens = Vale.objects.filter(query).values(
        'vale',
        'talao__talao',
        'status',
        'vale_entrega__data',
        'vale_entrega__user__first_name',
        'vale_entrega__user__last_name',
        'vale_entrega__combustivel__combustivel',
        'vale_entrega__posto__posto',
        'vale_entrega__valor',
        'vale_entrega__observacao',
    ).order_by('vale_entrega__data')

    paginator = Paginator(itens, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form': form,
        'form_submit_text': 'Filtrar',
    }
    context.update(menu)

    return render(request, 'talao/v2/consulta_vale.html', context)


@login_required()
@permission('patrimonio - combustivel - vale',)
def consulta_funcionarios(request):
    """
    View de exibição dos funcionários cadastrados
    :param request: informações gerais
    :return: template
    """
    menu = menu_consultas(request)

    q = request.GET.get('q', '')

    form = FormFiltraQ(
        'matrícula',
        initial={
            'q': q,
        }
    )

    query = Q()

    if q != '':
        query = query & Q(
            Q(username__icontains=q) |
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q)
        )

    itens = User.objects.filter(query).values(
        'username',
        'first_name',
        'last_name',
        'user_type__is_passive',
        'is_superuser',
        'is_active',
        'last_login',
    ).annotate(
        veiculos_qtde=Count(F('veiculos__id'))
    ).order_by('first_name', 'last_name')

    paginator = Paginator(itens, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form': form,
        'form_submit_text': 'Filtrar',
    }
    context.update(menu)

    return render(request, 'constel/v2/consulta_funcionarios.html', context)


@login_required()
@permission('patrimonio',)
def relatorios(request):
    context = menu_relatorios(request)

    return render(request, 'constel/v2/app.html', context)


@login_required()
@permission('patrimonio - combustivel - vale',)
def relatorio_mes(request):

    menu = menu_relatorios(request)

    hoje = datetime.date.today()

    itens = User.objects.filter(
        vale_user_to__data__month=hoje.month,
        vale_user_to__data__year=hoje.year,
    ).values(
        'username',
        'first_name',
        'last_name',
    ).annotate(
        total=Sum('vale_user_to__valor'),
        max_data=Max('vale_user_to__data'),
        n_vales=Count('vale_user_to__valor'),
    ).order_by(
        '-total'
    )

    paginator = Paginator(itens, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    context.update(menu)

    return render(request, 'talao/v2/relatorio_mes.html', context)


@login_required()
@permission('patrimonio - combustivel - vale',)
def relatorio_geral(request):

    menu = menu_relatorios(request)

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

    query = Q(vale_user_to__vale__status=2)

    if funcionario != '':
        query = query & Q(
            Q(username__icontains=funcionario) |
            Q(first_name__icontains=funcionario) |
            Q(last_name__icontains=funcionario))

    if data_inicial != '':
        data_inicial = datetime.datetime.strptime(data_inicial, "%Y-%m-%d").date()
        query = query & Q(vale_user_to__data__gte=data_inicial)

    if data_final != '':
        data_final = datetime.datetime.strptime(data_final, "%Y-%m-%d").date()
        query = query & Q(vale_user_to__data__lte=data_final)

    itens = User.objects.filter(query).values(
        'username',
        'first_name',
        'last_name',
    ).annotate(
        total=Sum('vale_user_to__valor'),
        max_data=Max('vale_user_to__data'),
        n_vales=Count('vale_user_to__valor'),
    ).order_by(
        '-total'
    )

    paginator = Paginator(itens, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form': form,
        'form_submit_text': 'Filtrar',
    }
    context.update(menu)

    return render(request, 'talao/v2/relatorio_geral.html', context)


@login_required()
@permission('patrimonio - combustivel - vale',)
def relatorio_geral_detalhe(request, user):

    menu = menu_relatorios(request)

    q = request.GET.get('q', '')

    form = FormFiltraQ(
        'código do vale ou matrícula',
        initial={
            'q': q,
        }
    )

    query = Q(vale_entrega__user_to__username=user)

    if q != '':
        query = query & Q(
            Q(vale__icontains=q) |
            Q(vale_entrega__user__username__icontains=q)
        )

    itens = Vale.objects.filter(query).values(
        'vale',
        'talao__talao',
        'status',
        'vale_entrega__data',
        'vale_entrega__user__first_name',
        'vale_entrega__user__last_name',
        'vale_entrega__combustivel__combustivel',
        'vale_entrega__posto__posto',
        'vale_entrega__valor',
        'vale_entrega__observacao',
    ).order_by('vale_entrega__data')

    paginator = Paginator(itens, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form': form,
        'form_submit_text': 'Filtrar',
    }
    context.update(menu)

    return render(request, 'talao/v2/relatorio_geral_detalhe.html', context)


@login_required
@permission('patrimonio - combustivel', 'patrimonio - combustivel - talao', )
def view_cadastrar_talao(request):
    """
    View de carregamento e gestão do cadastro de novos talões,
    Deve ser acessada somente pelo adm e funcionários autorizados
    :param request: informações do formulário
    :return: carregamento do formulário
    """

    if request.method == 'POST':
        form = FormCadastraTalao(request.POST)

        if form.is_valid():
            # Registro do cadastro do novo talão
            talao = Talao.objects.create(talao=form.cleaned_data['talao'])
            talao.save()
            cadastro_talao = CadastroTalao(talao=talao, user=request.user)

            for i in range(form.cleaned_data['vale_inicial'], form.cleaned_data['vale_final'] + 1):
                vale = Vale.objects.create(vale=i, talao=talao)
                vale.save()

            cadastro_talao.save()
            return HttpResponseRedirect('/patrimonio/combustivel/menu-cadastros')

    else:
        form = FormCadastraTalao()

    context = {
        'form': form,
        'callback': 'gc_menu_cadastros',
        'button_submit_text': 'Cadastrar talão',
        'callback_text': 'Voltar',
    }

    return render(request, 'talao/cadastro_talao.html', context)


@login_required
@permission('patrimonio', 'patrimonio - combustivel', 'patrimonio - combustivel - talao', )
def view_cadastrar_combustivel(request):
    """
    View de carregamento e gestão de combustível novos cadastrados no sistema,
    deve ser acessado apenas pelo adm e funcionãrios autorizados
    :param request: informações do formulário
    :return: carregamento do formulário
    """

    if request.method == 'POST':
        # Registro do cadastro do combustível
        form = FormCadastraCombustivel(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/patrimonio/combustivel/menu-cadastros/')
    else:
        form = FormCadastraCombustivel()

    combustiveis = Combustivel.objects.all().values(
        'combustivel'
    )

    context = {
        'combustiveis': combustiveis,
        'form': form,
        'callback': 'gc_menu_cadastros',
        'button_submit_text': 'Cadastrar combustível',
        'callback_text': 'Voltar',
        'pagina_titulo': 'Combustível',
        'menu_titulo': 'Cadastro de combutível',
    }

    return render(request, 'talao/cadastro_combustivel.html', context)


@login_required
@permission('patrimonio', 'patrimonio - combustivel', 'patrimonio - combustivel - talao', )
def view_cadastrar_posto(request):
    """
    View de carregamento e gestão de combustível novos cadastrados no sistema,
    deve ser acessado apenas pelo adm e funcionãrios autorizados
    :param request: informações do formulário
    :return: carregamento do formulário
    """

    if request.method == 'POST':
        # Registro do cadastro do posto
        form = FormCadastraPosto(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/patrimonio/combustivel/menu-cadastros/')
    else:
        form = FormCadastraPosto()

    postos = Posto.objects.all().values(
        'posto',
    )

    context = {
        'postos': postos,
        'form': form,
        'callback': 'gc_menu_cadastros',
        'button_submit_text': 'Cadastrar posto',
        'callback_text': 'Voltar',
        'pagina_titulo': 'Combustível',
        'menu_titulo': 'Cadastro de posto',
    }

    return render(request, 'talao/cadastro_posto.html', context)


@login_required
@permission('patrimonio - combustivel', 'patrimonio - combustivel - talao', )
def view_entrega_talao(request):
    """
    View de carregamento e gestão de entrega de talões cadastrados no sistema,
    deve ser acessado apenas pelo adm e funcionãrios autorizados
    :param request: informações do formulário
    :return: carregamento do formulário
    """

    if request.method == 'POST':
        # Registro da entrega do talão
        form = FormEntregaTalao(request.POST)

        if form.is_valid():
            talao = form.cleaned_data['talao']
            talao.status = 1
            Vale.objects.filter(talao=talao).update(status=1)
            entrega_talao = EntregaTalao(
                talao=talao,
                user=request.user,
                user_to=form.cleaned_data['user_to'],
            )
            entrega_talao.save()
            talao.save()
            return HttpResponseRedirect('/patrimonio/combustivel/menu-taloes/')
    else:
        form = FormEntregaTalao()

    context = {
        'form': form,
        'callback': 'gc_menu_taloes',
        'button_submit_text': 'Entregar talão',
        'callback_text': 'Cancelar',
        'pagina_titulo': 'Combustível',
        'menu_titulo': 'Entrega de talão',
    }

    return render(request, 'talao/entrega_talao.html', context)


@login_required
@permission('patrimonio - combustivel - vale', )
def view_entrega_vale_1(request):
    """
    View de carregamento e gestão de entrega de vales cadastrados no sistema,
    deve ser acessado apenas pelo adm e funcionãrios autorizados
    :param request: informações do formulário
    :return: carregamento do formulário
    """

    if request.method == 'POST':
        initial = {
            'user_to': request.session.get('user_to', None),
            'vale': request.session.get('vale', None),
        }
        form = FormEntregaVale1(data=request.POST, user=request.user, initial=initial)

        if form.is_valid():
            # Registro da entrega do vale
            request.session['user_to'] = form.cleaned_data['user_to']
            request.session['vale'] = form.cleaned_data['vale']

            return HttpResponseRedirect('/patrimonio/combustivel/menu-vales/entrega-vale-2/')

    else:
        form = FormEntregaVale1(user=request.user)

    context = {
        'form': form,
        'pagina_titulo': 'Combustível',
        'menu_titulo': 'Entrega de vale',
        'callback': 'gc_menu_vales',
        'button_submit_text': 'Avançar',
        'callback_text': 'Cancelar',
    }

    return render(request, 'talao/entrega_vale1.html', context)


@login_required
@permission('patrimonio - combustivel - vale', )
def view_entrega_vale_2(request):

    if request.session.get('user_to') is None:

        return HttpResponseRedirect('/patrimonio/combustivel/menu-vales/entrega-vale-1/')

    vale = Vale.objects.get(id=request.session['vale'])
    user_to = User.objects.get(id=request.session['user_to'])

    if request.method == 'POST':
        form = FormEntregaVale2(user_to, request.POST)

        if form.is_valid():
            request.session.pop('vale')
            request.session.pop('user_to')

            vale.status = 2
            vale.save()

            EntregaVale(
                user=request.user,
                user_to=user_to,
                vale=vale,
                combustivel=form.cleaned_data['combustivel'],
                valor=form.cleaned_data['valor'],
                observacao=form.cleaned_data['observacao'],
                posto=Posto.objects.get(id=form.cleaned_data['posto']),
            ).save()

            return HttpResponseRedirect('/patrimonio/combustivel/menu-vales/')

    else:
        form = FormEntregaVale2(user_to)

    context = {
        'user_to': user_to,
        'vale': vale,
        'form': form,
        'pagina_titulo': 'Combustível',
        'menu_titulo': 'Entrega de vale',
        'callback': 'gc_menu_vales',
        'button_submit_text': 'Entregar vale',
        'callback_text': 'Cancelar',
    }

    return render(request, 'talao/entrega_vale2.html', context)


@login_required
@permission('patrimonio - combustivel', )
def view_taloes(request):
    """
    View de exibição dos talões cadastrados no sistema
    :param request: informações gerais
    :return: lista de talões cadastrados
    """

    taloes = Talao.objects.all().order_by('talao')

    taloes = taloes.values(
        'talao',
        'status',
        'talao_cadastro__data',
        'talao_cadastro__user__first_name',
        'talao_cadastro__user__last_name',
        'talao_entrega__data',
        'talao_entrega__user__first_name',
        'talao_entrega__user__last_name',
        'talao_entrega__user_to__first_name',
        'talao_entrega__user_to__last_name',
    )

    context = {
        'taloes': taloes,
        'pagina_titulo': 'Combustível',
        'menu_titulo': 'Talões',
    }

    return render(request, 'talao/consulta_taloes.html', context)


@login_required
@permission('patrimonio - combustivel', )
def view_talao(request, **kwargs):
    """
    View de exibição de informações de talão
    :param request: informações gerais
    :param kwargs: id do talão desejado
    :return: informações do talão requerido
    """

    talao_id = kwargs.get('talao_id')

    if Talao.objects.filter(talao=talao_id).exists():
        talao = Talao.objects.filter(talao=talao_id)
        vales = Vale.objects.filter(talao__talao=talao_id).order_by('vale')

        talao = talao.values(
            'talao',
            'status',
            'talao_cadastro__data',
            'talao_cadastro__user__first_name',
            'talao_cadastro__user__last_name',
            'talao_entrega__data',
            'talao_entrega__user__first_name',
            'talao_entrega__user__last_name',
            'talao_entrega__user_to__first_name',
            'talao_entrega__user_to__last_name',
        )

        vales = vales.values(
            'vale',
            'status',
            'vale_entrega__data',
            'vale_entrega__user_to__first_name',
            'vale_entrega__user_to__last_name',
            'vale_entrega__combustivel__combustivel',
            'vale_entrega__valor',
            'vale_entrega__observacao',
        )

        for vale in vales:
            if vale['vale_entrega__valor'] is not None:
                vale['vale_entrega__valor'] = 'R$ {:8.2f}'.format(vale['vale_entrega__valor'])

        context = {
            'taloes': talao,
            'vales': vales,
            'pagina_titulo': 'Combustível',
            'menu_titulo': 'Talão',
        }
        return render(request, 'talao/consulta_talao.html', context)

    else:

        return HttpResponseRedirect('/patrimonio/combustivel/menu-consultas/')


@login_required
@permission('patrimonio - combustivel', )
def view_meu_talao(request, **kwargs):
    """
    View de exibição de informações de talão
    :param request: informações gerais
    :param kwargs: id do talão desejado
    :return: informações do talão requerido
    """

    talao_id = kwargs.get('talao_id')

    if Talao.objects.filter(talao=kwargs.get('talao_id')).exists():
        talao = Talao.objects.filter(talao=kwargs.get('talao_id'))
        vales = Vale.objects.filter(talao__talao=talao_id).order_by('vale')

        talao = talao.values(
            'talao',
            'status',
            'talao_cadastro__data',
            'talao_cadastro__user__first_name',
            'talao_cadastro__user__last_name',
            'talao_entrega__data',
            'talao_entrega__user__first_name',
            'talao_entrega__user__last_name',
            'talao_entrega__user_to__first_name',
            'talao_entrega__user_to__last_name',
        )

        vales = vales.values(
            'vale',
            'status',
            'vale_entrega__data',
            'vale_entrega__user_to__first_name',
            'vale_entrega__user_to__last_name',
            'vale_entrega__combustivel__combustivel',
            'vale_entrega__valor',
            'vale_entrega__observacao',
        )

        for vale in vales:
            if vale['vale_entrega__valor'] is not None:
                vale['vale_entrega__valor'] = 'R$ {:8.2f}'.format(vale['vale_entrega__valor'])

        context = {
            'taloes': talao,
            'vales': vales,
            'pagina_titulo': 'Combustível',
            'menu_titulo': 'Talão',
        }
        return render(request, 'talao/consulta_meu_talao.html', context)

    else:

        return HttpResponseRedirect('/patrimonio/combustivel/menu-consultas/')


@login_required
@permission('patrimonio - combustivel', )
def view_meus_vales(request):
    """

    :param request:
    :return:
    """

    vales = Vale.objects.filter(vale_entrega__user_to=request.user).order_by('vale')
    vales = vales.values(
        'vale',
        'talao',
        'status',
        'vale_entrega__data',
        'vale_entrega__user__first_name',
        'vale_entrega__user__last_name',
        'vale_entrega__combustivel__combustivel',
        'vale_entrega__valor',
        'vale_entrega__observacao',
    )

    for vale in vales:
        vale['vale_entrega__valor'] = 'R$ {:8.2f}'.format(vale['vale_entrega__valor'])

    context = {
        'vales': vales,
        'pagina_titulo': 'Combustível',
        'menu_titulo': 'Meus vales recebidos',
    }

    return render(request, 'talao/consulta_meus_vales.html', context)


@login_required
@permission('patrimonio - combustivel', )
def view_meus_taloes(request):
    """
    View de exibição dos talões cadastrados no sistema
    :param request: informações gerais
    :return: lista de talões cadastrados
    """

    taloes = Talao.objects.filter(talao_entrega__user_to=request.user).order_by('talao')
    taloes = taloes.values(
        'talao',
        'status',
        'talao_cadastro__data',
        'talao_cadastro__user__first_name',
        'talao_cadastro__user__last_name',
        'talao_entrega__data',
        'talao_entrega__user__first_name',
        'talao_entrega__user__last_name',
        'talao_entrega__user_to__first_name',
        'talao_entrega__user_to__last_name',
    )

    context = {
        'taloes': taloes,
        'pagina_titulo': 'Combustível',
        'menu_titulo': 'Talões',
    }

    return render(request, 'talao/consulta_meus_taloes.html', context)


@login_required
@permission('patrimonio', 'patrimonio - combustivel', )
def view_relatorio_mensal(request):
    """
    :param request:
    :return:
    """
    hoje = datetime.date.today()

    vales = User.objects.filter(
        vale_user_to__data__month=hoje.month,
        vale_user_to__data__year=hoje.year,
    ).annotate(
        total=Sum('vale_user_to__valor'),
        max_data=Max('vale_user_to__data'),
        n_vales=Count('vale_user_to__valor'),
    ).order_by(
        '-total'
    )
    vales = vales.values(
        'username',
        'first_name',
        'last_name',
        'max_data',
        'total',
        'n_vales',
    )

    for vale in vales:
        vale['total'] = 'R$ {:8.2f}'.format(vale['total'])

    context = {
        'vales': vales,
        'pagina_titulo': 'Combustível',
        'menu_titulo': 'Resumo mensal',
    }

    return render(request, 'talao/relatorio_mensal.html', context)


@login_required
@permission('patrimonio', 'patrimonio - combustivel', )
def view_relatorio_beneficiarios(request):

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

    query = Q(vale_user_to__vale__status=2)

    if funcionario != '':
        query = query & Q(
            Q(username__icontains=funcionario) |
            Q(first_name__icontains=funcionario) |
            Q(last_name__icontains=funcionario))

    if data_inicial != '':
        data_inicial = datetime.datetime.strptime(data_inicial, "%Y-%m-%d").date()
        query = query & Q(vale_user_to__data__gte=data_inicial)

    if data_final != '':
        data_final = datetime.datetime.strptime(data_final, "%Y-%m-%d").date()
        query = query & Q(vale_user_to__data__lte=data_final)

    vales = User.objects.filter(query).annotate(
        total=Sum('vale_user_to__valor'),
        max_data=Max('vale_user_to__data'),
        n_vales=Count('vale_user_to__valor'),
    ).order_by(
        '-total'
    )

    vales = vales.values(
        'username',
        'first_name',
        'last_name',
        'max_data',
        'total',
        'n_vales',
    )

    for vale in vales:
        vale['total'] = 'R$ {:8.2f}'.format(vale['total'])

    context = {
        'pagina_titulo': 'Relatório geral',
        'button_submit_text': 'Filtrar',
        'form': form,
        'vales': vales,
    }

    return render(request, 'talao/relatorio_beneficiarios.html', context)


@login_required
@permission('patrimonio', 'patrimonio - combustivel', )
def view_relatorio_beneficiarios_detalhe(request, funcionario):

    data_inicial = request.GET.get('data_inicial', '')
    data_final = request.GET.get('data_final', '')

    form = FormDataInicialFinal(
        initial={
            'data_inicial': data_inicial,
            'data_final': data_final,
        }
    )

    query = Q(user_to__username=funcionario)

    if data_inicial != '':
        data_inicial = datetime.datetime.strptime(data_inicial, "%Y-%m-%d").date()
        query = query & Q(data__gte=data_inicial)

    if data_final != '':
        data_final = datetime.datetime.strptime(data_final, "%Y-%m-%d").date()
        query = query & Q(data__lte=data_final)

    vales = EntregaVale.objects.filter(query)

    vales = vales.values(
        'vale',
        'data',
        'user__first_name',
        'user__last_name',
        'user_to__first_name',
        'user_to__last_name',
        'valor',
        'combustivel__combustivel',
        'posto',
        'observacao',
    )

    for vale in vales:
        vale['valor'] = 'R$ {:8.2f}'.format(vale['valor'])

    context = {
        'pagina_titulo': 'Detalhe',
        'button_submit_text': 'Filtrar',
        'form': form,
        'vales': vales,
        'funcionario': funcionario,
    }

    return render(request, 'talao/relatorio_beneficiarios_detalhe.html', context)
