"""
Módulo que contém as configurações dos menus gerais do sistema
"""

def menu_principal(request):
    """
    Funcão que contém as configurações do menu principal do sistema.
    Retorna um dicionário com as configurações
    """

    menu_buttons = [
        {'link': '/almoxarifado', 'text': 'Almoxarifado'},
        {'link': '/patrimonio', 'text': 'Patrimônio'},
        {'link': '/admin', 'text': 'Administrativo'},
    ]

    button_return = {'link': '/', 'text': 'Tela principal'}

    context = {
        'app': 'Almoxarifado',
        'menu': 'Menu principal',
        'menu_buttons': menu_buttons,
        'button_return': button_return,
    }

    return context
