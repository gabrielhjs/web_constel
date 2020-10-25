from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.db.models import Q, Count, OuterRef, Subquery
from django.core.paginator import Paginator

from constel.forms import FormFiltraQ

from .forms import FormAssociaGrupo, FormAssociaUsuario
from .decorator import permission
from .menu import menu_principal


@login_required()
def acesso_negado(request):

    return render(request, 'controle_acessos/v2/acesso_restrito.html')


@login_required
@permission('admin',)
def index(request):
    context = menu_principal(request)

    return render(request, 'constel/v2/app.html', context)


@login_required
@permission('admin',)
def usuarios(request):
    menu = menu_principal(request)

    q = request.GET.get('q', '')

    initial = {
        'q': q
    }

    form = FormFiltraQ(
        initial=initial,
        descricao='matrícula ou nome'
    )

    query = Q()

    if q != '':
        query = query & Q(
            Q(username__icontains=q) |
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q))

    itens = User.objects.filter(query).values(
        'username',
        'first_name',
        'last_name',
    ).order_by(
        'first_name',
        'last_name',
    )

    paginator = Paginator(itens, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form': form,
        'form_submit_text': 'Filtrar',
    }
    context.update(menu)

    return render(request, 'controle_acessos/v2/usuarios.html', context)


@login_required
@permission('admin',)
def usuarios_grupos(request, username):
    menu = menu_principal(request)

    user = User.objects.get(username=username)

    if request.method == 'POST':

        if username == 'admin':
            messages.error(request, 'Negado')

            return HttpResponseRedirect(f'/administracao/acesso/usuarios/{username}?{request.GET.urlencode()}')

        form = FormAssociaGrupo(data=request.POST)

        grupo_id = request.POST.get('grupo_id', None)

        if grupo_id is not None:
            user.groups.remove(Group.objects.get(id=grupo_id))

            return HttpResponseRedirect(f'/administracao/acesso/usuarios/{username}?{request.GET.urlencode()}')

        if form.is_valid():
            user.groups.add(form.cleaned_data['grupo'])

    else:
        form = FormAssociaGrupo(groups=user.groups.values('name'))

    itens = user.groups.values('name', 'id').order_by('name')

    paginator = Paginator(itens, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'user': user,
        'form': form,
        'form_submit_text': 'Adicionar grupo',
    }
    context.update(menu)

    return render(request, 'controle_acessos/v2/usuarios_grupos.html', context)


@login_required
@permission('admin',)
def grupos(request):
    menu = menu_principal(request)

    q = request.GET.get('q', '')

    initial = {
        'q': q
    }

    form = FormFiltraQ(
        initial=initial,
        descricao='nome'
    )

    query = Q()

    if q != '':
        query = query & Q(name__icontains=q)

    sub_query = User.objects.filter(
        groups__id=OuterRef('pk')
    ).values(
        'groups__id'
    ).annotate(
        quantidade=Count('id')
    ).values(
        'quantidade'
    )

    itens = Group.objects.filter(query).values(
        'id',
        'name',
    ).annotate(
        quantidade=Subquery(sub_query)
    )

    paginator = Paginator(itens, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form': form,
        'form_submit_text': 'Filtrar',
    }
    context.update(menu)

    return render(request, 'controle_acessos/v2/grupos.html', context)


@login_required
@permission('admin',)
def grupos_usuarios(request, grupo):
    menu = menu_principal(request)

    grupo = Group.objects.get(id=grupo)

    if request.method == 'POST':

        if grupo.name == 'admin':
            messages.error(request, 'Negado')

            return HttpResponseRedirect(f'/administracao/acesso/grupos/{grupo.id}?{request.GET.urlencode()}')

        form = FormAssociaUsuario(data=request.POST)

        user_id = request.POST.get('user_id', None)

        if user_id is not None:
            user = User.objects.get(username=user_id)
            user.groups.remove(grupo)

            return HttpResponseRedirect(f'/administracao/acesso/grupos/{grupo.id}?{request.GET.urlencode()}')

        if form.is_valid():
            user = form.cleaned_data['user']
            user.groups.add(grupo)

            return HttpResponseRedirect(f'/administracao/acesso/grupos/{grupo.id}?{request.GET.urlencode()}')

    else:
        form = FormAssociaUsuario(User.objects.filter(groups__id=grupo.id).values('id'))

    itens = User.objects.filter(groups__id=grupo.id).values(
        'username',
        'first_name',
        'last_name'
    ).order_by('first_name', 'last_name')

    paginator = Paginator(itens, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'grupo': grupo,
        'form': form,
        'form_submit_text': 'Adicionar usuário',
    }
    context.update(menu)

    return render(request, 'controle_acessos/v2/grupos_usuarios.html', context)
