

def principal(request):

  menu_buttons = [
    {'link': '/patrimonio/combustivel/km/registros', 'text': 'Registrar quilometragem'},
    {'link': '/patrimonio/combustivel/km/consultas', 'text': 'Consultas'},
  ]
  button_return = {'link': '/patrimonio', 'text': 'Voltar'}

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
    {'link': '/patrimonio/combustivel/km/consultas/pendencias/hoje', 'text': 'Painel diário de pendências'}
  ]
  button_return = {'link': '/patrimonio/combustivel/km', 'text': 'Voltar'}

  context = {
    'app': 'Km',
    'menu': 'Consutas',
    'menu_buttons': menu_buttons,
    'button_return': button_return,
  }

  return context
