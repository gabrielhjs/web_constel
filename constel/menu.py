"""
Módulo que contém as configurações dos menus de administração do sistema
"""


def menu_principal(request):
    """
    Funcão que contém as configurações do menu de administração do sistema.
    Retorna um dicionário com as configurações
    """

    menu_buttons = [
        {'link': '/admin', 'text': 'Administração Django'},
        {'link': '/administracao/acesso', 'text': 'Controle de acessos'},
        {'link': '/administracao/usuarios', 'text': 'Usuários'},
    ]

    button_return = {'link': '/', 'text': 'Voltar'}

    context = {
        'app': 'Admin',
        'menu': 'Menu principal',
        'menu_buttons': menu_buttons,
        'button_return': button_return,
    }

    return context
