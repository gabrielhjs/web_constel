

def menu_principal(request):
    """
    Funcão que contém as configurações do menu principal do patrimônio.
    Retorna um dicionário com as configurações
    """

    menu_buttons = [
        {'link': '/patrimonio/combustivel/talao', 'text': 'Combustível'},
    ]
    button_return = {'link': '/', 'text': 'Voltar'}

    context = {
        'app': 'Patrimônio',
        'menu': 'Principal',
        'menu_buttons': menu_buttons,
        'button_return': button_return,
    }

    return context


def menu_cadastros(request):
    """
    Funcão que contém as configurações do menu de cadastros do patrimônio.
    Retorna um dicionário com as configurações
    """

    menu_buttons = [
        {'link': '/patrimonio/cadastros/ferramenta', 'text': 'Cadastrar ferramenta'},
        {'link': '/patrimonio/cadastros/patrimonio', 'text': 'Cadastrar patrimônio'},
    ]
    button_return = {'link': '/', 'text': 'Voltar'}

    context = {
        'app': 'Patrimônio',
        'menu': 'Cadastros',
        'menu_buttons': menu_buttons,
        'button_return': button_return,
    }

    return context
