# Generated by Django 3.0.7 on 2020-06-09 16:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cont', '0011_auto_20200609_1612'),
        ('almoxarifado', '0017_auto_20191221_1216'),
        ('lista_saida', '0006_auto_20200408_0806'),
    ]

    operations = [
        migrations.CreateModel(
            name='OntDefeitoLista',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(auto_now=True, verbose_name='Lista criada em')),
                ('fornecedor', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='cont_defeito_lista_retirada', to='almoxarifado.Fornecedor')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cont_defeito_lista_saida', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OntDefeitoItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lista', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cont_defeito_lista_itens', to='lista_saida.OntLista')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cont_defeito_material_listas', to='cont.Ont')),
            ],
        ),
    ]
