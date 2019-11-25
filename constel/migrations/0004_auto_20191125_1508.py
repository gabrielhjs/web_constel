# Generated by Django 2.2.7 on 2019-11-25 18:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('constel', '0003_veiculo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='veiculo',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='veiculos', to=settings.AUTH_USER_MODEL, verbose_name='Usuário'),
        ),
    ]
