# Generated by Django 3.0.7 on 2020-06-10 15:18

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('almoxarifado', '0001_initial'),
        ('cont', '0001_initial'),
        ('lista_saida', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OntDefeitoItem',
            new_name='DefeitoOntItem',
        ),
        migrations.RenameModel(
            old_name='OntDefeitoLista',
            new_name='DefeitoOntLista',
        ),
    ]
