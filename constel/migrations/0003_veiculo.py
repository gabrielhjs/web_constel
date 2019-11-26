# Generated by Django 2.2.7 on 2019-11-22 19:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('constel', '0002_auto_20191120_1427'),
    ]

    operations = [
        migrations.CreateModel(
            name='Veiculo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modelo', models.CharField(help_text='Modelo do veículo', max_length=30)),
                ('placa', models.CharField(help_text='Placa do veículo', max_length=8)),
                ('cor', models.CharField(help_text='Cor do veículo', max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='veiculos', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]