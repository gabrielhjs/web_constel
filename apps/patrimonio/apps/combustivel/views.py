from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from constel.objects import Button
from constel.apps.controle_acessos.decorator import permission


@login_required
@permission('patrimonio - combustivel', )
def view_menu_principal(request):
    """
    View de carregamento da página inicial do GC
    :param request: informações gerais
    :return: carregamento da página inicial
    """

    button_1 = Button('gc_menu_cadastros', 'Cadastros')
    button_2 = Button('gc_menu_taloes', 'Genrenciamento de talões')
    button_3 = Button('gc_menu_vales', 'Gerenciamento de vales')
    button_4 = Button('gc_menu_consultas', 'Consultas')
    button_5 = Button('gc_menu_relatorios', 'Relatórios')
    button_voltar = Button('patrimonio_menu_principal', 'Voltar')

    context = {
        'guia_titulo': 'Constel | Combustível',
        'pagina_titulo': 'Combustível',
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


@login_required
@permission('patrimonio - combustivel', )
def view_menu_cadastros(request):
    """
    View de carregamento da página de cadastros do GC
    :param request: informações gerais
    :return: carregamento da página de cadastro
    """

    button_1 = Button('cadastra_usuario_passivo', 'Cadastrar beneficiário')
    button_2 = Button('cadastra_veiculo', 'Cadastrar veículo de beneficiário')
    button_3 = Button('gc_cadastro_combustivel', 'Cadastrar combustível')
    button_4 = Button('gc_cadastro_posto', 'Cadastrar posto')
    button_5 = Button('gc_cadastro_talao', 'Cadastrar talão')
    button_voltar = Button('gc_menu_principal', 'Voltar')

    context = {
        'guia_titulo': 'Constel | Combustível',
        'pagina_titulo': 'Combustível',
        'menu_titulo': 'Menu cadastros',
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


@login_required
@permission('patrimonio - combustivel', )
def view_menu_consultas(request):
    """
    View de carregamento da página de consultas do GC
    :param request: informações gerais
    :return: carregamento da página de consultas
    """

    button_1 = Button('gc_consulta_taloes', 'Talões')
    button_2 = Button('gc_consulta_meus_taloes', 'Meus talões recebidos')
    button_3 = Button('gc_consulta_meus_vales', 'Meus vales recebidos')
    button_4 = Button('consulta_funcionarios', 'Funcionários', 'gc_menu_consultas')
    button_5 = Button('consulta_veiculos', 'Veículos', 'gc_menu_consultas')
    button_voltar = Button('gc_menu_principal', 'Voltar')

    context = {
        'guia_titulo': 'Constel | Combustível',
        'pagina_titulo': 'Combustível',
        'menu_titulo': 'Menu consultas',
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


@login_required
@permission('patrimonio', 'patrimonio - combustivel', )
def view_menu_relatorios(request):
    """
    View de carregamento da página de relatórios do GC
    :param request: informações gerais
    :return: carregamento da página de relatórios
    """

    button_1 = Button('gc_relatorio_mensal', 'Acumulativo do mês')
    button_2 = Button('gc_relatorio_beneficiarios', 'Geral de beneficiários')
    button_voltar = Button('gc_menu_principal', 'Voltar')

    context = {
        'guia_titulo': 'Constel | Combustível',
        'pagina_titulo': 'Combustível',
        'menu_titulo': 'Menu relatórios',
        'buttons': [
            button_1,
            button_2,
        ],
        'rollback': button_voltar,
    }

    return render(request, 'constel/menu.html', context)


@login_required
@permission('patrimonio - combustivel', 'patrimonio - combustivel - talao', )
def view_menu_taloes(request):
    """
    View de carregamento da página de gerenciamento de talões do GC
    :param request: informações gerais
    :return: carregamento da página de gerenciamento de talões
    """

    button_1 = Button('gc_entrega_talao', 'Entregar talão')
    button_voltar = Button('gc_menu_principal', 'Voltar')

    context = {
        'guia_titulo': 'Constel | Combustível',
        'pagina_titulo': 'Combustível',
        'menu_titulo': 'Menu de talões',
        'buttons': [
            button_1,
        ],
        'rollback': button_voltar,
    }

    return render(request, 'constel/menu.html', context)


@login_required
@permission('patrimonio - combustivel', )
def view_menu_vales(request):
    """
    View de carregamento da página de gerenciamento de vales do GC
    :param request: informações gerais
    :return: carregamento da página de gerenciamento de vales
    """

    button_1 = Button('gc_entrega_vale_1', 'Entregar vale')
    button_voltar = Button('gc_menu_principal', 'Voltar')

    context = {
        'guia_titulo': 'Constel | Combustível',
        'pagina_titulo': 'Combustível',
        'menu_titulo': 'Menu consultas',
        'buttons': [
            button_1,
        ],
        'rollback': button_voltar,
    }

    return render(request, 'constel/menu.html', context)
