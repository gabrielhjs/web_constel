from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db.models import Sum, Max
from django.db.models import Q

import datetime

from .forms import *
from .models import Talao, Vale, CadastroTalao, EntregaTalao, EntregaVale, Combustivel
from constel.apps.controle_acessos.decorator import permission


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
        form = FormTalao(request.POST)

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
        form = FormTalao()

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

    context = {
        'combustiveis': Combustivel.objects.all(),
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

    context = {
        'postos': Posto.objects.all(),
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
    context = {
        'taloes': taloes,
        'pagina_titulo': 'Combustível',
        'menu_titulo': 'Talões',
    }

    return render(request, 'talao/consulta_talao.html', context)


@login_required
@permission('patrimonio - combustivel', )
def view_talao(request, **kwargs):
    """
    View de exibição de informações de talão
    :param request: informações gerais
    :param kwargs: id do talão desejado
    :return: informações do talão requerido
    """

    if Talao.objects.filter(talao=kwargs.get('talao_id')).exists():
        talao = Talao.objects.get(talao=kwargs.get('talao_id'))
        vales = Vale.objects.filter(talao=talao).order_by('vale')

        context = {
            'talao': talao,
            'vales': vales,
            'pagina_titulo': 'Combustível',
            'menu_titulo': 'Talão',
        }
        return render(request, 'talao/detalhes_talao.html', context)

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

    if Talao.objects.filter(talao=kwargs.get('talao_id')).exists():
        talao = Talao.objects.get(talao=kwargs.get('talao_id'))
        vales = Vale.objects.filter(talao=talao).order_by('vale')

        context = {
            'talao': talao,
            'vales': vales,
            'pagina_titulo': 'Combustível',
            'menu_titulo': 'Talão',
        }
        return render(request, 'talao/detalhes_meu_talao.html', context)

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
    context = {
        'taloes': taloes,
        'pagina_titulo': 'Combustível',
        'menu_titulo': 'Talões',
    }

    return render(request, 'talao/consulta_meus_talao.html', context)


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
        total=Sum('vale_user_to__valor')
    ).order_by(
        '-total'
    )

    for vale in vales:
        vale.total = 'R$ {:8.2f}'.format(vale.total)

    context = {
        'vales': vales,
        'pagina_titulo': 'Combustível',
        'menu_titulo': 'Resumo mensal',
    }

    return render(request, 'talao/relatorio_mensal.html', context)


@login_required
@permission('patrimonio', 'patrimonio - combustivel', )
def view_relatorio_por_periodo(request):

    context = {}

    if request.method == 'POST':
        form = FormRelatorioPeriodo(request.POST)

        if form.is_valid():
            data_inicial = form.cleaned_data['data_inicial']
            data_final = form.cleaned_data['data_final']

            vales = User.objects.filter(
                vale_user_to__data__gte=data_inicial,
                vale_user_to__data__lte=data_final,
            ).annotate(
                total=Sum('vale_user_to__valor')
            ).order_by(
                '-total'
            )

            for vale in vales:
                vale.total = 'R$ {:8.2f}'.format(vale.total)

            context.update({'vales': vales, })

    form = FormRelatorioPeriodo()

    context.update({
        'pagina_titulo': 'Relatório por data',
        'button_submit_text': 'Pesquisar',
        'form': form,
    })

    return render(request, 'talao/relatorio_por_periodo.html', context)


@login_required
@permission('patrimonio', 'patrimonio - combustivel', )
def view_relatorio_por_funcionario(request):

    data_inicial = request.GET.get('data_inicial', '')
    data_final = request.GET.get('data_final', '')
    funcionario = request.GET.get('funcionario', '')

    form = FormRelatorioFuncionario(
        initial={
            'data_inicial': data_inicial,
            'data_final': data_final,
            'funcionario': funcionario,
        }
    )

    if data_inicial != '':
        data_inicial = datetime.datetime.strptime(data_inicial, "%Y-%m-%d").date()

    if data_final != '':
        data_final = datetime.datetime.strptime(data_final, "%Y-%m-%d").date()

    context = {}

    print(data_inicial, data_final, funcionario)

    if funcionario != '' and data_inicial != '' and data_final != '':
        queryset = Q(username__contains=funcionario) & \
                   Q(vale_user_to__data__gte=data_inicial) & \
                   Q(vale_user_to__data__lte=data_final)

    elif funcionario != '' and data_inicial != '':
        queryset = Q(username__contains=funcionario) & \
                   Q(vale_user_to__data__gte=data_inicial)

    elif funcionario != '' and data_final != '':
        queryset = Q(username__contains=funcionario) & \
                   Q(vale_user_to__data__lte=data_final)

    elif data_inicial != '' and data_final != '':
        queryset = Q(vale_user_to__data__gte=data_inicial) & \
                   Q(vale_user_to__data__lte=data_final)

    elif data_inicial != '':
        queryset = Q(vale_user_to__data__gte=data_inicial)

    elif data_final != '':
        queryset = Q(vale_user_to__data__lte=data_final)

    elif funcionario != '':
        queryset = Q(username__contains=funcionario)

    else:
        queryset = Q(vale_user_to__data__gte=datetime.datetime.strptime('2018-01-01', "%Y-%m-%d").date())

    vales = User.objects.filter(
        queryset
    ).annotate(
        total=Sum('vale_user_to__valor'),
        data=Max('vale_user_to__data')
    ).order_by(
        '-total'
    )

    for vale in vales:
        vale.total = 'R$ {:8.2f}'.format(vale.total)

    context.update({
        'pagina_titulo': 'Relatório geral',
        'button_submit_text': 'Filtrar',
        'form': form,
        'vales': vales
    })

    return render(request, 'talao/relatorio_beneficiarios.html', context)
