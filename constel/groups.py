from django.contrib.auth.models import Group, User, Permission


def set_groups():
    group_gerencia_gc = Group.objects.create(name='gerencia_gc')
    group_patrimonio = Group.objects.create(name='patrimonio')
    group_combustivel_gerencia_talao = Group.objects.create(name='combustivel_gerencia_talao')
    group_combustivel_gerencia_vale = Group.objects.create(name='combustivel_gerencia_vale')
    group_combustivel_beneficiario = Group.objects.create(name='combustivel_beneficiario')

    group_combustivel_gerencia_talao.permissions.add(
        Permission.objects.get(codename='add_cadastrotalao'),
        Permission.objects.get(codename='view_cadastrotalao'),
        Permission.objects.get(codename='add_entregatalao'),
        Permission.objects.get(codename='view_entregatalao'),
        Permission.objects.get(codename='add_talao'),
        Permission.objects.get(codename='change_talao'),
        Permission.objects.get(codename='view_talao'),
        Permission.objects.get(codename='add_vale'),
        Permission.objects.get(codename='view_vale'),
    )

    group_combustivel_gerencia_vale.permissions.add(
        Permission.objects.get(codename='add_entregavale'),
        Permission.objects.get(codename='view_entregavale'),
        Permission.objects.get(codename='change_vale'),
        Permission.objects.get(codename='view_vale'),
        Permission.objects.get(codename='add_vale'),
    )

    group_combustivel_beneficiario.permissions.add(
        Permission.objects.get(codename='view_vale'),
    )

    groups = [
        group_gerencia_gc,
        group_patrimonio,
        group_combustivel_gerencia_talao,
        group_combustivel_gerencia_vale,
        group_combustivel_beneficiario,
    ]

    admin = User.objects.get(username='admin')

    for group in groups:
        group.user_set.add(admin)
