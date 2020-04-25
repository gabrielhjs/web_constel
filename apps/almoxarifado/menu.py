"""
Módulo que contém as configurações dos menus gerais do sistema
"""

def menu_principal(request):
    """
    Funcão que contém as configurações do menu principal do almoxarifado.
    Retorna um dicionário com as configurações
    """

    menu_buttons = [
        {'link': '/almoxarifado/cont', 'text': 'Cont2'},
        {'link': '/almoxarifado/cadastros', 'text': 'Cadastros'},
        {'link': '/almoxarifado/menu-entradas', 'text': 'Entradas'},
        {'link': '/almoxarifado/menu-saidas', 'text': 'Saídas'},
        {'link': '/almoxarifado/menu-consultas', 'text': 'Consultas'},
        {'link': '/almoxarifado/menu-relatorios', 'text': 'Relatórios'},
    ]
    button_return = {'link': '/', 'text': 'Voltar'}

    context = {
        'app': 'Almoxarifado',
        'menu': 'Principal',
        'menu_buttons': menu_buttons,
        'button_return': button_return,
    }

    return context


def menu_cadastros(request):
    """
    Funcão que contém as configurações do menu de cadastros do almoxarifado.
    Retorna um dicionário com as configurações
    """

    menu_buttons = [
        {'link': '/almoxarifado/cadastros/material', 'text': 'Cadastrar material'},
        {'link': '/almoxarifado/cadastros/fornecedor', 'text': 'Cadastrar fornecedor'},
    ]
    button_return = {'link': '/almoxarifado', 'text': 'Voltar'}

    context = {
        'app': 'Almoxarifado',
        'menu': 'Cadastros',
        'menu_buttons': menu_buttons,
        'button_return': button_return,
    }

    return context
