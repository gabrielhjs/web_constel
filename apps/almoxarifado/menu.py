"""
Módulo que contém as configurações dos menus gerais do almoxarifado
"""


def menu_principal(request):
    """
    Funcão que contém as configurações do menu principal do almoxarifado.
    Retorna um dicionário com as configurações
    """

    menu_buttons = [
        {'link': '/almoxarifado/cont', 'text': 'Cont2'},
        {'link': '/almoxarifado/cadastros', 'text': 'Cadastros'},
        {'link': '/almoxarifado/edicao', 'text': 'Edição'},
        {'link': '/almoxarifado/entradas/material', 'text': 'Entrada de material'},
        {'link': '/almoxarifado/saidas/material/lista', 'text': 'Saída de material'},
        {'link': '/almoxarifado/consultas', 'text': 'Consultas'},
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


def menu_edicao(request):
    """
    Funcão que contém as configurações do menu de edição do almoxarifado.
    Retorna um dicionário com as configurações
    """

    menu_buttons = [
        {'link': '/almoxarifado/edicao/material', 'text': 'Editar materiais'},
        # {'link': '/almoxarifado/edicao/fornecedor', 'text': 'Editar fornecedores'},
    ]
    button_return = {'link': '/almoxarifado', 'text': 'Voltar'}

    context = {
        'app': 'Almoxarifado',
        'menu': 'Edição',
        'menu_buttons': menu_buttons,
        'button_return': button_return,
    }

    return context


def menu_consultas(request):
    """
    Funcão que contém as configurações do menu de consultas do almoxarifado.
    Retorna um dicionário com as configurações
    """

    menu_buttons = [
        {'link': '/almoxarifado/consultas/estoque', 'text': 'Estoque materiais'},
        {'link': '/almoxarifado/consultas/ordens/entradas', 'text': 'Registro de entradas'},
        {'link': '/almoxarifado/consultas/ordens/saidas', 'text': 'Registro de saídas'},
        {'link': '/almoxarifado/consultas/funcionarios/', 'text': 'Funcionários'},
        {'link': '/almoxarifado/consultas/fornecedores/', 'text': 'Fornecedores'},
        {'link': '/almoxarifado/consultas/materiais/saidas/', 'text': 'Saída de materiais'},
    ]
    button_return = {'link': '/almoxarifado', 'text': 'Voltar'}

    context = {
        'app': 'Almoxarifado',
        'menu': 'Consultas',
        'menu_buttons': menu_buttons,
        'button_return': button_return,
    }

    return context
