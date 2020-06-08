from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q, Max
from django.core.paginator import Paginator
from django.conf import settings

from .forms import *
from .models import Secao, Modelo
from .menu import menu_principal, menu_cadastros, menu_consultas

from constel.apps.controle_acessos.decorator import permission
from constel.forms import FormFuncionario


@login_required()
@permission('almoxarifado', )
def index(request):
    context = menu_principal(request)

    return render(request, 'constel/v2/app.html', context)


@login_required()
@permission('almoxarifado', )
def cadastros(request):
    context = menu_cadastros(request)

    return render(request, 'constel/v2/app.html', context)


@login_required()
@permission('almoxarifado', )
def cadastrar_secao(request):
    menu = menu_cadastros(request)

    if request.method == 'POST':
        form = FormCadastraSecao(request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/almoxarifado/cont/menu-cadastros/')
    else:
        form = FormCadastraSecao()

    itens = Secao.objects.all().values(
        'nome',
        'descricao',
        'data',
    ).order_by('nome', 'descricao')

    paginator = Paginator(itens, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form': form,
        'form_submit_text': 'Cadastrar seção',
    }
    context.update(menu)

    return render(request, 'cont/v2/cadastra_secao.html', context)


@login_required()
@permission('almoxarifado', )
def cadastrar_modelo(request):
    menu = menu_cadastros(request)

    if request.method == 'POST':
        form = FormCadastraModelo(request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/almoxarifado/cont/menu-cadastros/')
    else:
        form = FormCadastraModelo()

    itens = Modelo.objects.all().values(
        'nome',
        'descricao',
        'data',
    ).order_by('nome', 'descricao')

    paginator = Paginator(itens, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form': form,
        'form_submit_text': 'Cadastrar modelo',
    }
    context.update(menu)

    return render(request, 'cont/v2/cadastra_modelo.html', context)


@login_required()
@permission('almoxarifado', )
def entrada_1(request):
    menu = menu_principal(request)

    if request.method == 'POST':
        initial = {
            'modelo': request.session.get('cont2_entrada_modelo', None),
            'secao': request.session.get('cont2_entrada_secao', None),
        }
        form = FormEntradaOnt1(data=request.POST, initial=initial)

        if form.is_valid():
            request.session['cont2_entrada_modelo'] = form.cleaned_data['modelo']
            request.session['cont2_entrada_secao'] = form.cleaned_data['secao']

            return HttpResponseRedirect('/almoxarifado/cont/entrada-2')
    else:
        form = FormEntradaOnt1()

    context = {
        'form': form,
        'form_submit_text': 'Avançar',
    }
    context.update(menu)

    return render(request, 'cont/v2/entrada_1.html', context)


@login_required()
@permission('almoxarifado', )
def entrada_2(request):
    menu = menu_principal(request)

    if request.session.get('cont2_entrada_modelo') is None or request.session.get('cont2_entrada_secao') is None:

        return HttpResponseRedirect('/almoxarifado/cont/entrada-1/')

    modelo = Modelo.objects.get(id=request.session['cont2_entrada_modelo'])
    secao = Secao.objects.get(id=request.session['cont2_entrada_secao'])

    if request.method == 'POST':
        form = FormEntradaOnt2(request.POST)

        if form.is_valid():
            serial = form.cleaned_data['serial'].upper()
            if Ont.objects.filter(codigo=serial).exists():
                ont = Ont.objects.get(codigo=serial)

                if ont.status != 0 or ont.secao != secao or ont.modelo != modelo:

                    if ont.status != 0:
                        ont.status = 0
                        OntEntrada(ont=ont, user=request.user).save()
                        messages.success(request, 'Ont (RE)inserida no estoque com sucesso')

                    if ont.secao != secao:
                        ont.secao = secao
                        messages.success(request, 'Seção da ONT alterada')

                    if ont.modelo != modelo:
                        ont.modelo = modelo
                        messages.success(request, 'Modelo da ONT alterado!')
                
                    ont.save()
                    OntEntradaHistorico(ont=ont, user=request.user).save()

                else:
                    messages.error(request, 'Serial de Ont já em estoque')

            else:
                ont = Ont(
                    codigo=serial,
                    status=0,
                    modelo=modelo,
                    secao=secao,
                )
                ont.save()

                messages.success(request, 'Ont cadastrada e inserida no estoque com sucesso!')

                OntEntrada(ont=ont, user=request.user).save()
                OntEntradaHistorico(ont=ont, user=request.user).save()

            return HttpResponseRedirect('/almoxarifado/cont/entrada-2/')

    else:
        form = FormEntradaOnt2()

    historico = OntEntradaHistorico.objects.filter(user=request.user).order_by('id').values(
        'ont__codigo',
    )

    context = {
        'form': form,
        'form_submit_text': 'Inserir',
        'callback': 'almoxarifado_cont_entrada_ont_3',
        'modelo': modelo.nome,
        'secao': secao.nome,
        'historico': historico,
    }
    context.update(menu)

    return render(request, 'cont/v2/entrada_2.html', context)


@login_required()
@permission('almoxarifado', )
def entrada_3(request):

    OntEntradaHistorico.objects.filter(user=request.user).delete()
    request.session.pop('cont2_entrada_modelo')
    request.session.pop('cont2_entrada_secao')

    return HttpResponseRedirect('/almoxarifado/cont/entrada-1')


@login_required()
@permission('almoxarifado', )
def consultas(request):
    context = menu_consultas(request)

    return render(request, 'constel/v2/app.html', context)


@login_required()
@permission('almoxarifado', )
def consulta_status(request):
    menu = menu_consultas(request)

    onts = Ont.objects.all()

    onts_status_secao_modelo = onts.values(
        'status',
        'secao__nome',
        'modelo__nome',
        'secao__id',
        'modelo__id',
    ).annotate(
        Count('codigo')
    ).order_by(
        'status',
        'secao__nome',
        'modelo__nome',
    )

    context = {
        'onts_status_secao_modelo': onts_status_secao_modelo,
    }
    context.update(menu)

    return render(request, 'cont/v2/consulta_status.html', context)


@login_required()
@permission('almoxarifado', )
def consulta_status_detalhe(request, status, secao, modelo):
    menu = menu_consultas(request)

    itens = Ont.objects.filter(
        status=status,
    ).filter(
        secao__id=secao,
        modelo__id=modelo,
    ).values(
        'codigo',
    ).annotate(
        max_data=Max('entrada_ont__data')
    ).order_by(
        'max_data',
    )
    
    paginator = Paginator(itens, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    context.update(menu)

    return render(request, 'cont/v2/consulta_status_detalhe.html', context)


@login_required()
@permission('almoxarifado', )
def consulta_tecnicos_carga(request):
    menu = menu_consultas(request)

    funcionario = request.GET.get('funcionario', '')

    form = FormFuncionario(initial={'funcionario': funcionario})

    query = Q()

    if funcionario != '':
        query = query & Q(
            Q(username__icontains=funcionario) |
            Q(first_name__icontains=funcionario) |
            Q(last_name__icontains=funcionario))

    sub_query = OntSaida.objects.filter(
        ont__status=1
    ).values(
        'ont__codigo',
    ).annotate(
        max_id=Max('id'),
    ).values(
        'max_id'
    )

    itens = User.objects.filter(
        query,
        saida_user_to__id__in=sub_query,
    ).annotate(
        total=Count('saida_user_to__data', distinct=True),
        max_data=Max('saida_user_to__data'),
    ).values(
        'username',
        'first_name',
        'last_name',
        'max_data',
        'total',
    ).order_by(
        '-total',
    )

    paginator = Paginator(itens, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form_submit_text': 'Filtrar',
        'form': form,
    }
    context.update(menu)

    return render(request, 'cont/v2/consulta_tecnicos_carga.html', context)


@login_required()
@permission('almoxarifado', )
def consulta_tecnicos_carga_detalhe(request, funcionario):
    menu = menu_consultas(request)

    sub_query = OntSaida.objects.filter(
        ont__status=1
    ).values(
        'ont__codigo',
    ).annotate(
        max_id=Max('id'),
    ).values(
        'max_id'
    )

    carga = OntSaida.objects.filter(
        user_to__username=funcionario,
        id__in=sub_query,
    ).values(
        'ont__codigo',
        'user__first_name',
        'user__last_name',
        'user_to__first_name',
        'user_to__last_name',
    ).annotate(
        max_data=Max('data')
    ).order_by(
        '-max_data'
    )

    funcionario = User.objects.get(username=funcionario)

    funcionario = {
        'first_name': funcionario.first_name,
        'last_name': funcionario.last_name,
    }

    paginator = Paginator(carga, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'funcionario': funcionario,
    }
    context.update(menu)

    return render(request, 'cont/v2/consulta_tecnicos_carga_detalhe.html', context)


@login_required()
@permission('almoxarifado', )
def view_dashboard(request):
    pass


@login_required()
def baixa_login_psw(request):
    menu = menu_principal(request)

    if request.method == 'POST':
        initial = {
            'username': request.session.get('psw_username', ''),
            'password': request.session.get('psw_password', ''),
        }
        form = FormPswLogin(request.POST, initial=initial)

        if form.is_valid():
            request.session['psw_username'] = form.cleaned_data['username']
            request.session['psw_password'] = form.cleaned_data['password']

            return HttpResponseRedirect('/almoxarifado/cont/baixa/psw-contrato')

    else:
        form = FormPswLogin()

    context = {
        'form': form,
        'form_submit_text': 'Logar',
    }
    context.update(menu)

    return render(request, 'cont/v2/psw_login.html', context)


@login_required()
def baixa_busca_contrato(request):
    menu = menu_principal(request)

    psw_username = request.session.get('psw_username', None),
    psw_password = request.session.get('psw_password', None),

    if psw_username is None or psw_password is None:
        return HttpResponseRedirect('/almoxarifado/cont/baixa/psw-login')

    if request.method == 'POST':
        form = FormPswContrato(request.POST)

    else:
        form = FormPswContrato()

    context = {
        'form': form,
        'form_submit_text': 'Buscar',
        'psw_username': request.session.get('psw_username'),
        'psw_password': request.session.get('psw_password'),
        'ws_url': settings.CONTWE2_URL,
        'ws_token': settings.CONTWE2_TOKEN,
    }
    context.update(menu)

    return render(request, 'cont/v2/psw_contrato.html', context)
