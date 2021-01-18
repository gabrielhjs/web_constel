# Generated by Django 3.0.7 on 2021-01-18 07:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('patrimonio', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Patrimonio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, verbose_name='Nome')),
                ('descricao', models.TextField(max_length=500, verbose_name='Descrição')),
                ('data', models.DateTimeField(auto_now=True, verbose_name='Data de entrada')),
                ('valor', models.FloatField(default=0)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='patrimonios_cadastrados', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PatrimonioEntrada1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observacao', models.TextField(blank=True, max_length=500, null=True, verbose_name='Observação')),
                ('data', models.DateTimeField(auto_now=True, verbose_name='Data de entrada')),
            ],
        ),
        migrations.CreateModel(
            name='PatrimonioId',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, 'Estoque'), (1, 'Em uso'), (2, 'Defeito'), (2, 'Manutenção'), (3, 'Inutilizado')], default=0)),
                ('codigo', models.IntegerField(default=0, verbose_name='Código')),
                ('patrimonio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patrimonio_id', to='patrimonio1.Patrimonio')),
            ],
        ),
        migrations.CreateModel(
            name='PatrimonioSaida',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observacao', models.TextField(blank=True, max_length=500, null=True, verbose_name='Observação')),
                ('data', models.DateTimeField(auto_now=True, verbose_name='Data de saída')),
                ('entrada', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='patrimonio_entrada_saida', to='patrimonio1.PatrimonioEntrada1', verbose_name='Patrimônio')),
                ('ordem', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='saida_ordem_patrimonio', to='patrimonio.Ordem')),
                ('patrimonio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patrimonio_saida', to='patrimonio1.PatrimonioId')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='patrimonio_saidas', to=settings.AUTH_USER_MODEL)),
                ('user_to', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='patrimonio_retiradas', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PatrimonioEntradaHistorico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patrimonio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patrimonio_historico_entrada', to='patrimonio1.PatrimonioId')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='entrada_historico_patrimonio', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='patrimonioentrada1',
            name='patrimonio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patrimonio_entrada', to='patrimonio1.PatrimonioId'),
        ),
        migrations.AddField(
            model_name='patrimonioentrada1',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='user_entrada_patrimonio', to=settings.AUTH_USER_MODEL),
        ),
    ]
