

def principal(request):

  menu_buttons = [
    {'link': '/patrimonio/combustivel/km/registros', 'text': 'Registrar quilometragem'},
    {'link': '/patrimonio/combustivel/km/edicoes', 'text': 'Edição'},
    {'link': '/patrimonio/combustivel/km/consultas', 'text': 'Consultas'},
    {'link': '/patrimonio/combustivel/km/relatorios', 'text': 'Relatórios'},
  ]
  button_return = {'link': '/patrimonio/combustivel/talao', 'text': 'Voltar'}

  context = {
    'app': 'Km',
    'menu': 'Principal',
    'menu_buttons': menu_buttons,
    'button_return': button_return,
  }

  return context


def registros(request):

  menu_buttons = [
    {'link': '/patrimonio/combustivel/km/registros/inicial', 'text': 'Inicial dia'},
    {'link': '/patrimonio/combustivel/km/registros/final', 'text': 'Final dia'},
    {'link': '/patrimonio/combustivel/km/registros/falta', 'text': 'Falta'},
  ]
  button_return = {'link': '/patrimonio/combustivel/km', 'text': 'Voltar'}

  context = {
    'app': 'Km',
    'menu': 'Registros',
    'menu_buttons': menu_buttons,
    'button_return': button_return,
  }

  return context


def consultas(request):

  menu_buttons = [
    {'link': '/patrimonio/combustivel/km/consultas/equipe', 'text': 'Minha equipe'},
    {'link': '/patrimonio/combustivel/km/consultas/hoje', 'text': 'Registros de hoje'},
    {'link': '/patrimonio/combustivel/km/consultas/pendencias/hoje', 'text': 'Painel diário de pendências'},
    {'link': '/patrimonio/combustivel/km/consultas/registros', 'text': 'Registros'},
  ]
  button_return = {'link': '/patrimonio/combustivel/km', 'text': 'Voltar'}

  context = {
    'app': 'Km',
    'menu': 'Consutas',
    'menu_buttons': menu_buttons,
    'button_return': button_return,
  }

  return context


def edicoes(request):

  menu_buttons = [
    {'link': '/patrimonio/combustivel/km/edicoes/registro', 'text': 'Editar registro'},
  ]
  button_return = {'link': '/patrimonio/combustivel/km', 'text': 'Voltar'}

  context = {
    'app': 'Km',
    'menu': 'Edições',
    'menu_buttons': menu_buttons,
    'button_return': button_return,
  }

  return context


def relatorios(request):

  menu_buttons = [
    {'link': '/patrimonio/combustivel/km/relatorios/geral', 'text': 'Geral'},
  ]
  button_return = {'link': '/patrimonio/combustivel/km', 'text': 'Voltar'}

  context = {
    'app': 'Km',
    'menu': 'Relatórios',
    'menu_buttons': menu_buttons,
    'button_return': button_return,
  }

  return context
