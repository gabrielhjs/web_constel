# Generated by Django 3.0.7 on 2020-12-14 00:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('patrimonio1', '0001_initial'),
        ('ferramenta', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lista',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(auto_now=True, verbose_name='Lista criada em')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_patrimonio_lista', to=settings.AUTH_USER_MODEL)),
                ('user_to', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='user_to_patrimonio_lista', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ItemPatrimonio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lista', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lista_patrimonios', to='lista_saida_patrimonio.Lista')),
                ('patrimonio', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='patrimonio1.PatrimonioId')),
            ],
        ),
        migrations.CreateModel(
            name='ItemFerramenta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField(default=1)),
                ('ferramenta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ferramenta.Ferramenta')),
                ('lista', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lista_ferramentas', to='lista_saida_patrimonio.Lista')),
            ],
        ),
    ]
