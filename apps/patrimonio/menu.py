

def menu_principal(request):
    """
    Funcão que contém as configurações do menu principal do patrimônio.
    Retorna um dicionário com as configurações
    """

    menu_buttons = [
        {'link': '/patrimonio/combustivel/talao', 'text': 'Combustível'},
        {'link': '/patrimonio/cadastros', 'text': 'Cadastros'},
        {'link': '/patrimonio/entradas', 'text': 'Entradas'},
        {'link': '/patrimonio/saidas', 'text': 'Saídas'},
        {'link': '/patrimonio/consultas', 'text': 'Consultas'},
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
        {'link': '/patrimonio/cadastros/patrimonio', 'text': 'Cadastrar modelo de patrimônio'},
    ]
    button_return = {'link': '/patrimonio', 'text': 'Voltar'}

    context = {
        'app': 'Patrimônio',
        'menu': 'Cadastros',
        'menu_buttons': menu_buttons,
        'button_return': button_return,
    }

    return context


def menu_entradas(request):
    """
    Funcão que contém as configurações do menu de entradas do patrimônio.
    Retorna um dicionário com as configurações
    """

    menu_buttons = [
        {'link': '/patrimonio/entradas/ferramenta', 'text': 'Entrada de ferramenta'},
        {'link': '/patrimonio/entradas/patrimonio', 'text': 'Entrada de patrimônio'},
    ]
    button_return = {'link': '/patrimonio', 'text': 'Voltar'}

    context = {
        'app': 'Patrimônio',
        'menu': 'Entradas',
        'menu_buttons': menu_buttons,
        'button_return': button_return,
    }

    return context


def menu_saidas(request):
    """
    Funcão que contém as configurações do menu de saídas do patrimônio.
    Retorna um dicionário com as configurações
    """

    menu_buttons = [
        {'link': '/patrimonio/saidas/ferramenta', 'text': 'Entrega de ferramenta'},
        {'link': '/patrimonio/saidas/patrimonio', 'text': 'Entrega de patrimônio'},
    ]
    button_return = {'link': '/patrimonio', 'text': 'Voltar'}

    context = {
        'app': 'Patrimônio',
        'menu': 'Saídas',
        'menu_buttons': menu_buttons,
        'button_return': button_return,
    }

    return context


def menu_consultas(request):
    """
    Funcão que contém as configurações do menu de consultas do patrimônio.
    Retorna um dicionário com as configurações
    """

    menu_buttons = [
        {'link': '/patrimonio/consultas/ferramenta', 'text': 'Modelos de ferramenta'},
        {'link': '/patrimonio/consultas/patrimonio', 'text': 'Modelos de patrimônio'},
        {'link': '/patrimonio/consultas/ferramenta/estoque', 'text': 'Estoque de ferramentas'},
        {'link': '/patrimonio/consultas/patrimonio/status', 'text': 'Status dos patrimônio'},
    ]
    button_return = {'link': '/patrimonio', 'text': 'Voltar'}

    context = {
        'app': 'Patrimônio',
        'menu': 'Consultas',
        'menu_buttons': menu_buttons,
        'button_return': button_return,
    }

    return context
