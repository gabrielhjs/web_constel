from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from constel.objects import Button
from constel.apps.controle_acessos.decorator import permission


@login_required
@permission('Admin', )
def view_menu_principal(request):

    button_1 = Button('gc_menu_principal', 'Controle de vales')
    button_2 = Button('patrimonio_menu_cadastros', 'Cadastros')
    button_3 = Button('patrimonio_menu_entradas', 'Entradas')
    button_4 = Button('patrimonio_menu_saidas', 'Saídas')
    button_5 = Button('patrimonio_menu_consultas', 'Consultas')
    button_6 = Button('patrimonio_menu_relatorios', 'Relatórios')
    button_voltar = Button('index', 'Voltar')

    context = {
        'guia_titulo': 'Constel | Patrimônio',
        'pagina_titulo': 'Patrimônio',
        'menu_titulo': 'Menu principal',
        'buttons': [
            button_1,
            button_2,
            button_3,
            button_4,
            button_5,
            # button_6,
        ],
        'rollback': button_voltar,
    }

    return render(request, 'constel/menu.html', context)


@login_required
def view_menu_cadastros(request):

    button_1 = Button('patrimonio_cadastrar_ferramenta', 'Cadastrar ferramenta')
    button_2 = Button('patrimonio_cadastrar_patrimonio', 'Cadastrar modelo de patrimônio')
    button_voltar = Button('patrimonio_menu_principal', 'Voltar')

    context = {
        'guia_titulo': 'Constel | Patrimônio',
        'pagina_titulo': 'Patrimônio',
        'menu_titulo': 'Menu cadastros',
        'buttons': [
            button_1,
            button_2,
        ],
        'rollback': button_voltar,
    }

    return render(request, 'constel/menu.html', context)


@login_required
def view_menu_entradas(request):

    button_1 = Button('patrimonio_entrada_ferramenta', 'Aquisição de ferramentas')
    button_2 = Button('patrimonio_entrada_patrimonio', 'Aquisição de patrimônio')
    button_voltar = Button('patrimonio_menu_principal', 'Voltar')

    context = {
        'guia_titulo': 'Constel | Patrimônio',
        'pagina_titulo': 'Patrimônio',
        'menu_titulo': 'Menu entradas',
        'buttons': [
            button_1,
            button_2,
        ],
        'rollback': button_voltar,
    }

    return render(request, 'constel/menu.html', context)


@login_required
def view_menu_saidas(request):

    button_1 = Button('patrimonio_saida_patrimonio', 'Saída de patrimônio')
    button_2 = Button('patrimonio_saida_ferramenta', 'Saída de ferramenta')
    button_voltar = Button('patrimonio_menu_principal', 'Voltar')

    context = {
        'guia_titulo': 'Constel | Patrimônio',
        'pagina_titulo': 'Patrimônio',
        'menu_titulo': 'Menu saídas',
        'buttons': [
            button_1,
            button_2,
        ],
        'rollback': button_voltar,
    }

    return render(request, 'constel/menu.html', context)


@login_required
def view_menu_consultas(request):

    button_1 = Button('patrimonio_consulta_ferramentas', 'Modelos de ferramentas cadastradas')
    button_2 = Button('patrimonio_consulta_patrimonios_modelos', 'Modelos de patrimônios cadastrados')
    button_3 = Button('patrimonio_consulta_ferramentas_estoque', 'Ferramentas estoque')
    button_4 = Button('patrimonio_consulta_patrimonios', 'Patrimônios datalhado')
    button_voltar = Button('patrimonio_menu_principal', 'Voltar')

    context = {
        'guia_titulo': 'Constel | Patrimônio',
        'pagina_titulo': 'Patrimônio',
        'menu_titulo': 'Menu saídas',
        'buttons': [
            button_1,
            button_2,
            button_3,
            button_4,
        ],
        'rollback': button_voltar,
    }

    return render(request, 'constel/menu.html', context)


@login_required
def view_menu_relatorios(request):

    return render(request, 'patrimonio/menu_relatorios.html')
