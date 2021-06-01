"""
Módulo que contém as configurações dos menus de controle de acesso do sistema
"""


def menu_principal(request):
    """
    Funcão que contém as configurações do menu principal do controle de acessos.
    Retorna um dicionário com as configurações
    """

    menu_buttons = [
        {'link': '/gerencia', 'text': 'Dashboard'},
        {'link': '/gerencia/painel-diario', 'text': 'Painel diário'},
    ]

    button_return = {'link': '/', 'text': 'Voltar'}

    context = {
        'app': 'Gerência',
        'menu': 'Menu principal',
        'menu_buttons': menu_buttons,
        'button_return': button_return,
    }

    return context
