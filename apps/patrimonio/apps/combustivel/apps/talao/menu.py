"""
Módulo que contém as configurações dos menus gerais do sistema
"""


def menu_principal(request):
    """
    Funcão que contém as configurações do menu principal do Controle de combustível.
    Retorna um dicionário com as configurações
    """

    menu_buttons = [
        {'link': '/patrimonio/combustivel/talao/cadastros', 'text': 'Cadastros'},
        {'link': '/patrimonio/combustivel/talao/taloes', 'text': 'Gerenciamento de talões'},
        {'link': '/patrimonio/combustivel/talao/vales', 'text': 'Gerenciamento de vales'},
        {'link': '/patrimonio/combustivel/talao/consultas', 'text': 'Consultas'},
        {'link': '/patrimonio/combustivel/talao/relatorios', 'text': 'Relatórios'},
    ]
    button_return = {'link': '/', 'text': 'Voltar'}

    context = {
        'app': 'Combustível',
        'menu': 'Principal',
        'menu_buttons': menu_buttons,
        'button_return': button_return,
    }

    return context


def menu_cadastros(request):
    """
    Funcão que contém as configurações do menu de cadastros do Controle de combustível.
    Retorna um dicionário com as configurações
    """

    menu_buttons = [
        {'link': '/cadusuario-pass', 'text': 'Cadastrar beneficiário'},
        {'link': '/cadveiculo', 'text': 'Cadastrar veículo de beneficiário'},
        {'link': '/patrimonio/combustivel/talao/combustivel', 'text': 'Cadastrar combustível'},
        {'link': '/patrimonio/combustivel/talao/posto', 'text': 'Cadastrar posto'},
        {'link': '/patrimonio/combustivel/talao/talao', 'text': 'Cadastrar talão'},
    ]
    button_return = {'link': '/patrimonio/combustivel/talao', 'text': 'Voltar'}

    context = {
        'app': 'Combustível',
        'menu': 'Cadastros',
        'menu_buttons': menu_buttons,
        'button_return': button_return,
    }

    return context


def menu_consultas(request):
    """
    Funcão que contém as configurações do menu de consultas do Controle de combustível.
    Retorna um dicionário com as configurações
    """

    menu_buttons = [
        {'link': '/almoxarifado/cont/consultas/situacao', 'text': 'Status'},
        {'link': '/almoxarifado/cont/consultas/cargas', 'text': 'Cargas de ONT\'s'},
        {'link': '/almoxarifado/cont/consultas/ont', 'text': 'Busca serial'},
        {'link': '/almoxarifado/cont/consultas/dashboard', 'text': 'Dashboard'},
    ]
    button_return = {'link': '/patrimonio/combustivel/talao', 'text': 'Voltar'}

    context = {
        'app': 'Combustível',
        'menu': 'Consultas',
        'menu_buttons': menu_buttons,
        'button_return': button_return,
    }

    return context
