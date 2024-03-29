

def menu_principal(request):
    """
    Funcão que contém as configurações do menu principal do patrimônio.
    Retorna um dicionário com as configurações
    """

    menu_buttons = [
        {'link': '/patrimonio/combustivel/talao', 'text': 'Combustível'},
        {'link': '/patrimonio/cadastros', 'text': 'Cadastros'},
        {'link': '/patrimonio/entradas', 'text': 'Entradas'},
        {'link': '/patrimonio/saidas/lista', 'text': 'Saídas'},
        {'link': '/patrimonio/fechamento/ferramenta', 'text': 'Fechamento (ferramentas)'},
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
        {'link': '/patrimonio/entradas/patrimonio_1', 'text': 'Entrada de patrimônio'},
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
        {'link': '/patrimonio/consultas/modelos', 'text': 'Modelos'},
        {'link': '/patrimonio/consultas/ferramenta/estoque', 'text': 'Estoque de ferramentas'},
        {'link': '/patrimonio/consultas/patrimonio/status', 'text': 'Status de patrimônio'},
        {'link': '/patrimonio/consultas/saidas', 'text': 'Registro de saídas'},
        {'link': '/patrimonio/consultas/colaboradores', 'text': 'Colaboradores'},
    ]
    button_return = {'link': '/patrimonio', 'text': 'Voltar'}

    context = {
        'app': 'Patrimônio',
        'menu': 'Consultas',
        'menu_buttons': menu_buttons,
        'button_return': button_return,
    }

    return context


def menu_consultas_modelos(request):
    """
    Funcão que contém as configurações do menu de consultas de modelos do patrimônio.
    Retorna um dicionário com as configurações
    """

    menu_buttons = [
        {'link': '/patrimonio/consultas/ferramenta', 'text': 'Ferramentas'},
        {'link': '/patrimonio/consultas/patrimonio', 'text': 'Patrimônio'},
    ]
    button_return = {'link': '/patrimonio/consultas', 'text': 'Voltar'}

    context = {
        'app': 'Patrimônio',
        'menu': 'Modelos',
        'menu_buttons': menu_buttons,
        'button_return': button_return,
    }

    return context
