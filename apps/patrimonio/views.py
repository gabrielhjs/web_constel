from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required()
def view_menu_principal(request):

    return render(request, 'patrimonio/menu_principal.html')


@login_required()
def view_menu_cadastros(request):

    return render(request, 'patrimonio/menu_cadastros.html')


@login_required()
def view_menu_entradas(request):

    return render(request, 'patrimonio/menu_entradas.html')


@login_required()
def view_menu_consultas(request):

    return render(request, 'patrimonio/menu_consultas.html')


@login_required()
def view_menu_relatorios(request):

    return render(request, 'patrimonio/menu_relatorios.html')
