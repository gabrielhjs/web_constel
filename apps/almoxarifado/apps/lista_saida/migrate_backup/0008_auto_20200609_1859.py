# Generated by Django 3.0.7 on 2020-06-09 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lista_saida', '0007_ontdefeitoitem_ontdefeitolista'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ontdefeitoitem',
            name='lista',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cont_defeito_lista_itens', to='lista_saida.OntDefeitoLista'),
        ),
    ]
