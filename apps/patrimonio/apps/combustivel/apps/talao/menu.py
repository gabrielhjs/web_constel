"""
Módulo que contém as configurações dos menus gerais do sistema
"""


def menu_principal(request):
    """
    Funcão que contém as configurações do menu principal do Controle de combustível.
    Retorna um dicionário com as configurações
    """

    menu_buttons = [
        {'link': '/patrimonio/combustivel/talao/cadastros', 'text': 'Cadastros'},
        {'link': '/patrimonio/combustivel/talao/taloes', 'text': 'Gerenciamento de talões'},
        {'link': '/patrimonio/combustivel/talao/vales', 'text': 'Gerenciamento de vales'},
        {'link': '/patrimonio/combustivel/cartao', 'text': 'Gerenciamento de cartão'},
        {'link': '/patrimonio/combustivel/talao/consultas', 'text': 'Consultas'},
        {'link': '/patrimonio/combustivel/talao/relatorios', 'text': 'Relatórios'},
    ]
    button_return = {'link': '/', 'text': 'Voltar'}

    context = {
        'app': 'Combustível',
        'menu': 'Principal',
        'menu_buttons': menu_buttons,
        'button_return': button_return,
    }

    return context


def menu_cadastros(request):
    """
    Funcão que contém as configurações do menu de cadastros do Controle de combustível.
    Retorna um dicionário com as configurações
    """

    menu_buttons = [
        {'link': '/patrimonio/combustivel/talao/cadastros/beneficiario', 'text': 'Cadastrar beneficiário'},
        {'link': '/patrimonio/combustivel/talao/cadastros/veiculo', 'text': 'Cadastrar veículo de beneficiário'},
        {'link': '/patrimonio/combustivel/talao/cadastros/combustivel', 'text': 'Cadastrar combustível'},
        {'link': '/patrimonio/combustivel/talao/cadastros/posto', 'text': 'Cadastrar posto'},
        {'link': '/patrimonio/combustivel/talao/cadastros/talao', 'text': 'Cadastrar talão'},
    ]
    button_return = {'link': '/patrimonio/combustivel/talao', 'text': 'Voltar'}

    context = {
        'app': 'Combustível',
        'menu': 'Cadastros',
        'menu_buttons': menu_buttons,
        'button_return': button_return,
    }

    return context


def menu_taloes(request):
    """
    Funcão que contém as configurações do menu de gerenciamento de talão do Controle de combustível.
    Retorna um dicionário com as configurações
    """

    menu_buttons = [
        {'link': '/patrimonio/combustivel/talao/taloes/entrega', 'text': 'Entregar talão'},
        {'link': '/patrimonio/combustivel/talao/taloes/devolucao', 'text': 'Devolução de talão vazio'},
    ]
    button_return = {'link': '/patrimonio/combustivel/talao', 'text': 'Voltar'}

    context = {
        'app': 'Combustível',
        'menu': 'Talões',
        'menu_buttons': menu_buttons,
        'button_return': button_return,
    }

    return context


def menu_vales(request):
    """
    Funcão que contém as configurações do menu de gerenciamento de vale do Controle de combustível.
    Retorna um dicionário com as configurações
    """

    menu_buttons = [
        {'link': '/patrimonio/combustivel/talao/vales/entrega-1', 'text': 'Entregar vale'},
        {'link': '/patrimonio/combustivel/talao/vales/edicao/', 'text': 'Editar vale entregue'},
    ]
    button_return = {'link': '/patrimonio/combustivel/talao', 'text': 'Voltar'}

    context = {
        'app': 'Combustível',
        'menu': 'Vales',
        'menu_buttons': menu_buttons,
        'button_return': button_return,
    }

    return context


def menu_consultas(request):
    """
    Funcão que contém as configurações do menu de consultas do Controle de combustível.
    Retorna um dicionário com as configurações
    """

    menu_buttons = [
        {'link': '/patrimonio/combustivel/talao/consultas/taloes', 'text': 'Talões'},
        {'link': '/patrimonio/combustivel/talao/consultas/vales', 'text': 'Vales'},
        {'link': '/patrimonio/combustivel/cartao/consultas/depositos', 'text': 'Depósitos'},
        {'link': '/patrimonio/combustivel/talao/consultas/usuario/taloes', 'text': 'Meus talões'},
        {'link': '/patrimonio/combustivel/talao/consultas/usuario/vales', 'text': 'Meus vales'},
        {'link': '/patrimonio/combustivel/talao/consultas/funcionarios', 'text': 'Funcionários'},
    ]
    button_return = {'link': '/patrimonio/combustivel/talao', 'text': 'Voltar'}

    context = {
        'app': 'Combustível',
        'menu': 'Consultas',
        'menu_buttons': menu_buttons,
        'button_return': button_return,
    }

    return context


def menu_relatorios(request):
    """
    Funcão que contém as configurações do menu de relatórios do Controle de combustível.
    Retorna um dicionário com as configurações
    """

    menu_buttons = [
        {'link': '/patrimonio/combustivel/talao/relatorios/mes', 'text': 'Mensal'},
        {'link': '/patrimonio/combustivel/talao/relatorios/geral', 'text': 'Geral'},
    ]
    button_return = {'link': '/patrimonio/combustivel/talao', 'text': 'Voltar'}

    context = {
        'app': 'Combustível',
        'menu': 'Relatórios',
        'menu_buttons': menu_buttons,
        'button_return': button_return,
    }

    return context
