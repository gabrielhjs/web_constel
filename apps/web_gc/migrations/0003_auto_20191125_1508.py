# Generated by Django 2.2.7 on 2019-11-25 18:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_gc', '0002_auto_20191118_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talao',
            name='talao',
            field=models.IntegerField(help_text='Insira um valor válido de talão', unique=True, validators=[django.core.validators.MinValueValidator(1, 'Talão inválido'), django.core.validators.MaxValueValidator(999999, 'Talão inválido')], verbose_name='Talao'),
        ),
        migrations.AlterField(
            model_name='vale',
            name='vale',
            field=models.IntegerField(unique=True, validators=[django.core.validators.MinValueValidator(10000, 'Vale inválido'), django.core.validators.MaxValueValidator(9999999, 'Vale inválido')]),
        ),
    ]
