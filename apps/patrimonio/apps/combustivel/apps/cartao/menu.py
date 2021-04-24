"""
Módulo que contém as configurações dos menus gerais do sistema
"""


def menu_principal(request):
    """
    Funcão que contém as configurações do menu principal do Controle de cartão combustível.
    Retorna um dicionário com as configurações
    """

    menu_buttons = [
        {'link': '/patrimonio/combustivel/cartao/importar', 'text': 'Importar dados'},
    ]
    button_return = {'link': '/patrimonio/combustivel/talao', 'text': 'Voltar'}

    context = {
        'app': 'Cartão',
        'menu': 'Principal',
        'menu_buttons': menu_buttons,
        'button_return': button_return,
    }

    return context
