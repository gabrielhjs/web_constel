# Generated by Django 2.2.7 on 2019-12-13 16:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patrimonio', '0011_auto_20191213_1245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patrimonioentrada',
            name='patrimonio',
        ),
        migrations.RemoveField(
            model_name='patrimonioentrada',
            name='user',
        ),
        migrations.RemoveField(
            model_name='patrimoniosaida',
            name='entrada',
        ),
        migrations.RemoveField(
            model_name='patrimoniosaida',
            name='patrimonio',
        ),
        migrations.RemoveField(
            model_name='patrimoniosaida',
            name='user',
        ),
        migrations.RemoveField(
            model_name='patrimoniosaida',
            name='user_to',
        ),
        migrations.DeleteModel(
            name='Patrimonio',
        ),
        migrations.DeleteModel(
            name='PatrimonioEntrada',
        ),
        migrations.DeleteModel(
            name='PatrimonioSaida',
        ),
    ]