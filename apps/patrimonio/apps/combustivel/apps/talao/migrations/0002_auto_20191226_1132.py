# Generated by Django 2.2.7 on 2019-12-26 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talao', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='combustivel',
            name='combustivel',
            field=models.CharField(error_messages={'unique': 'Este combustível já está cadastrado no sistema!'}, help_text='Insira um combustível', max_length=30, unique=True),
        ),
    ]
