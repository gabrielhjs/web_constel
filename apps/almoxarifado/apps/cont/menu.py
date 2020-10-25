"""
Módulo que contém as configurações dos menus gerais do sistema
"""


def menu_principal(request):
    """
    Funcão que contém as configurações do menu principal do Cont2.
    Retorna um dicionário com as configurações
    """

    menu_buttons = [
        {'link': '/almoxarifado/cont/cadastros', 'text': 'Cadastros'},
        {'link': '/almoxarifado/cont/entrada-1', 'text': 'Entrada de ONT\'s'},
        {'link': '/almoxarifado/cont/saidas/lista', 'text': 'Saída de ONT\'s'},
        {'link': '/almoxarifado/cont/baixa/psw-login', 'text': 'Aplicação de ONT\'s'},
        {'link': '/almoxarifado/cont/fechamentos', 'text': 'Fechamento de ONT\'s'},
        {'link': '/almoxarifado/cont/consultas', 'text': 'Consultas'},
    ]
    button_return = {'link': '/', 'text': 'Voltar'}

    context = {
        'app': 'Cont2',
        'menu': 'Principal',
        'menu_buttons': menu_buttons,
        'button_return': button_return,
    }

    return context


def menu_cadastros(request):
    """
    Funcão que contém as configurações do menu de cadastros do Cont2.
    Retorna um dicionário com as configurações
    """

    menu_buttons = [
        {'link': '/almoxarifado/cont/cadastros/secao', 'text': 'Cadastrar seção'},
        {'link': '/almoxarifado/cont/cadastros/modelo', 'text': 'Cadastrar modelo de ONT\'s'},
    ]
    button_return = {'link': '/almoxarifado/cont', 'text': 'Voltar'}

    context = {
        'app': 'Cont2',
        'menu': 'Cadastros',
        'menu_buttons': menu_buttons,
        'button_return': button_return,
    }

    return context


def menu_consultas(request):
    """
    Funcão que contém as configurações do menu de consultas do Cont2.
    Retorna um dicionário com as configurações
    """

    menu_buttons = [
        {'link': '/almoxarifado/cont/consultas/situacao', 'text': 'Status'},
        {'link': '/almoxarifado/cont/consultas/cargas', 'text': 'Cargas de ONT\'s'},
        {'link': '/almoxarifado/cont/consultas/saidas', 'text': 'Registro de saídas'},
        {'link': '/almoxarifado/cont/consultas/ont', 'text': 'Busca serial'},
        {'link': '/almoxarifado/cont/consultas/dashboard', 'text': 'Dashboard'},
    ]
    button_return = {'link': '/almoxarifado/cont', 'text': 'Voltar'}

    context = {
        'app': 'Cont2',
        'menu': 'Consultas',
        'menu_buttons': menu_buttons,
        'button_return': button_return,
    }

    return context


def menu_fechamento(request):
    """
    Funcão que contém as configurações do menu de fechamento de onts do Cont2.
    Retorna um dicionário com as configurações
    """

    menu_buttons = [
        {'link': '/almoxarifado/cont/fechamento/entrada/defeito', 'text': 'Entrada de ONT\'s com defeito'},
        {'link': '/almoxarifado/cont/fechamento/entrada/manutencao_1', 'text': 'Entrada de ONT\'s de manutenção'},
        {'link': '/almoxarifado/cont/defeito/saidas/lista', 'text': 'Devolução de ONT\'s com defeito'},
        {'link': '/almoxarifado/cont/manutencao/saidas/lista', 'text': 'Devolução de ONT\'s de manutenção'},
    ]
    button_return = {'link': '/almoxarifado/cont', 'text': 'Voltar'}

    context = {
        'app': 'Cont2',
        'menu': 'Defeitos',
        'menu_buttons': menu_buttons,
        'button_return': button_return,
    }

    return context
