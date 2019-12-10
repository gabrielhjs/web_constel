# Generated by Django 2.2.7 on 2019-12-10 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patrimonio', '0006_auto_20191210_1453'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ferramentaquantidade',
            old_name='quandidade',
            new_name='quantidade',
        ),
        migrations.AlterField(
            model_name='ferramentaentrada',
            name='valor',
            field=models.FloatField(default=0, verbose_name='Valor total'),
        ),
    ]
