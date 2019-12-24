from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from constel.objects import Button


@login_required()
def view_menu_principal(request):

    button_vales = Button('gc_menu_principal', 'Controle de vales')
    button_cadastros = Button('patrimonio_menu_cadastros', 'Cadastros')
    button_entradas = Button('patrimonio_menu_entradas', 'Entradas')
    button_saidas = Button('patrimonio_menu_saidas', 'Saídas')
    button_consultas = Button('patrimonio_menu_consultas', 'Consultas')
    button_relatorios = Button('patrimonio_menu_relatorios', 'Relatórios')
    button_voltar = Button('index', 'Voltar')

    context = {
        'admin': request.user.is_superuser,
        'guia_titulo': 'Constel | Patrimônio',
        'menu_titulo': 'Patrimônio',
        'buttons': [
            button_vales,
            button_cadastros,
            button_entradas,
            button_saidas,
            button_consultas,
            button_relatorios,
        ],
        'rollback': button_voltar,
    }

    return render(request, 'constel/menu.html', context)


@login_required()
def view_menu_cadastros(request):

    return render(request, 'patrimonio/menu_cadastros.html')


@login_required()
def view_menu_entradas(request):

    return render(request, 'patrimonio/menu_entradas.html')


@login_required()
def view_menu_saidas(request):

    return render(request, 'patrimonio/menu_saidas.html')


@login_required()
def view_menu_consultas(request):

    return render(request, 'patrimonio/menu_consultas.html')


@login_required()
def view_menu_relatorios(request):

    return render(request, 'patrimonio/menu_relatorios.html')
