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
        {'link': '/administracao/cadastro', 'text': 'Cadastros'},
    ]

    button_return = {'link': '/', 'text': 'Voltar'}

    context = {
        'app': 'Administração',
        'menu': 'Menu principal',
        'menu_buttons': menu_buttons,
        'button_return': button_return,
    }

    return context


def menu_cadastros(request):
    """
    Funcão que contém as configurações do menu de administração do sistema.
    Retorna um dicionário com as configurações
    """

    menu_buttons = [
        {'link': '/administracao/usuarios/cadastro/sem_acesso', 'text': 'Cadastro de funcionário sem acesso'},
        # {'link': '/administracao/usuarios/cadastro/cargo', 'text': 'Cadastro de gargo'},
    ]

    button_return = {'link': '/administracao', 'text': 'Voltar'}

    context = {
        'app': 'Administração',
        'menu': 'Cadastros',
        'menu_buttons': menu_buttons,
        'button_return': button_return,
    }

    return context

