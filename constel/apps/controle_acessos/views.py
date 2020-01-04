from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User

from constel.objects import Button
from .forms import FormCriaGrupo, FormAssociaGrupo
from .decorator import permission


@login_required()
@permission('admin', )
def view_menu_controle_acessos(request):
    button_1 = Button('constel_controle_menu_grupos', 'Gerenciamento de grupo de acessos')
    rollback = Button('constel_menu_admin', 'Voltar')

    context = {
        'guia_titulo': 'Constel | Admin',
        'pagina_titulo': 'Controle de Acessos',
        'menu_titulo': 'Menu principal',
        'buttons': [
            button_1,
        ],
        'rollback': rollback,
    }

    return render(request, 'constel/menu.html', context)


@login_required()
@permission('admin', )
def view_menu_grupos(request):

    button_1 = Button('constel_controle_grupos_criar', 'Criar novo grupo')
    button_2 = Button('constel_controle_grupos_usuarios', 'Usuários')
    rollback = Button('constel_menu_controle_acessos', 'Voltar')

    context = {
        'guia_titulo': 'Constel | Admin',
        'pagina_titulo': 'Controle de Acessos',
        'menu_titulo': 'Menu de grupos',
        'buttons': [
            button_1,
            button_2,
        ],
        'rollback': rollback,
    }

    return render(request, 'constel/menu.html', context)


@login_required()
@permission('admin', )
def view_grupos_criar(request):

    if request.method == 'POST':
        form = FormCriaGrupo(request.POST)

        if form.is_valid():
            Group.objects.create(
                name=form.cleaned_data['nome']
            ).save()

            return HttpResponseRedirect('/menu-admin/controle-acessos/grupos/')

    else:
        form = FormCriaGrupo()

    context = {
        'form': form,
        'callback': 'constel_controle_menu_grupos',
        'callback_text': 'Cancelar',
        'button_submit_text': 'Criar grupo',
        'pagina_titulo': 'Controle de Acessos',
        'menu_titulo': 'Criar grupo',
        'grupos': Group.objects.all(),
    }

    return render(request, 'controle_acessos/cria_grupo.html', context)


@login_required()
@permission('admin', )
def view_grupos_usuarios(request):

    usuarios = User.objects.filter(is_active=True).order_by('first_name', 'last_name')

    context = {
        'usuarios': usuarios,
        'pagina_titulo': 'Controle de Acessos',
        'menu_titulo': 'Usuários',
    }

    return render(request, 'controle_acessos/usuarios.html', context)


@login_required()
@permission('admin', )
def view_grupos_usuario(request, usuario_id):

    usuario = User.objects.get(id=usuario_id)
    grupos = usuario.groups.all().order_by('name')

    if request.method == 'POST':
        grupo_id = request.POST.get('grupo_id', None)

        if grupo_id is not None:
            usuario.groups.remove(Group.objects.get(id=grupo_id))

            return HttpResponseRedirect('/menu-admin/controle-acessos/grupos/usuario/' + str(usuario.id))

        form = FormAssociaGrupo(request.POST)

        if form.is_valid():
            usuario.groups.add(Group.objects.get(id=form.cleaned_data['grupo']))

    else:
        form = FormAssociaGrupo()

    context = {
        'form': form,
        'callback': 'constel_controle_grupos_usuarios',
        'callback_text': 'Voltar',
        'button_submit_text': 'Adidicionar grupo',
        'grupos': grupos,
        'pagina_titulo': 'Controle de Acessos',
        'menu_titulo': usuario.first_name.title() + ' ' + usuario.last_name.title(),
    }

    return render(request, 'controle_acessos/usuario.html', context)


@login_required()
def view_acesso_negado(request):

    return render(request, 'controle_acessos/acesso_negado.html')
