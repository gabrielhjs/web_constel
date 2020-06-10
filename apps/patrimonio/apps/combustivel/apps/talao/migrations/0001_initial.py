# Generated by Django 3.0.7 on 2020-06-10 16:01

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Combustivel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('combustivel', models.CharField(error_messages={'unique': 'Este combustível já está cadastrado no sistema!'}, help_text='Insira um combustível', max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Posto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posto', models.CharField(max_length=100, verbose_name='Posto')),
                ('rua', models.CharField(max_length=255)),
                ('numero', models.IntegerField(verbose_name='N°')),
                ('cidade', models.CharField(default='Curitiba', max_length=255)),
                ('estado', models.CharField(default='Paraná', max_length=255)),
                ('pais', models.CharField(default='Brasil', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Talao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('talao', models.IntegerField(help_text='Insira um valor válido de talão', unique=True, validators=[django.core.validators.MinValueValidator(1, 'Talão inválido'), django.core.validators.MaxValueValidator(999999, 'Talão inválido')], verbose_name='Talao')),
                ('status', models.IntegerField(choices=[(0, 'Disponível'), (1, 'Em uso'), (2, 'Usado')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Vale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vale', models.IntegerField(unique=True, validators=[django.core.validators.MinValueValidator(10000, 'Vale inválido'), django.core.validators.MaxValueValidator(9999999, 'Vale inválido')])),
                ('status', models.IntegerField(choices=[(0, 'Indisponível'), (1, 'Disponível'), (2, 'Usado')], default=0)),
                ('talao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='talao_vales', to='talao.Talao')),
            ],
        ),
        migrations.CreateModel(
            name='EntregaVale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(auto_now=True)),
                ('valor', models.FloatField(null=True)),
                ('observacao', models.TextField(blank=True, max_length=255, verbose_name='Observações')),
                ('combustivel', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='talao.Combustivel', verbose_name='Combustível')),
                ('posto', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='vale_posto', to='talao.Posto')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='vale_user', to=settings.AUTH_USER_MODEL)),
                ('user_to', models.ForeignKey(default=None, help_text='Usuário que irá receber o vale combustível', on_delete=django.db.models.deletion.PROTECT, related_name='vale_user_to', to=settings.AUTH_USER_MODEL, verbose_name='Para')),
                ('vale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vale_entrega', to='talao.Vale')),
            ],
        ),
        migrations.CreateModel(
            name='EntregaTalao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(auto_now=True)),
                ('talao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='talao_entrega', to='talao.Talao')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='talao_user', to=settings.AUTH_USER_MODEL)),
                ('user_to', models.ForeignKey(default=None, help_text='Usuário que irá receber o talão', on_delete=django.db.models.deletion.PROTECT, related_name='talao_user_to', to=settings.AUTH_USER_MODEL, verbose_name='Para')),
            ],
        ),
        migrations.CreateModel(
            name='CadastroTalao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(auto_now=True)),
                ('talao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='talao_cadastro', to='talao.Talao')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
