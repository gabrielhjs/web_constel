

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
    {'link': '/patrimonio/combustivel/km/registros/inicial', 'text': 'Quilometragem inicial'},
    {'link': '/patrimonio/combustivel/km/registros/final', 'text': 'Quilometragem final'},
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

  ]
  button_return = {'link': '/patrimonio/combustivel/km', 'text': 'Voltar'}

  context = {
    'app': 'Km',
    'menu': 'Consutas',
    'menu_buttons': menu_buttons,
    'button_return': button_return,
  }

  return context
