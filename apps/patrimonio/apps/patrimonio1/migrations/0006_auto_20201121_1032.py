# Generated by Django 3.0.7 on 2020-11-21 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patrimonio1', '0005_auto_20200825_1025'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patrimonioid',
            name='valor',
        ),
        migrations.AddField(
            model_name='patrimonio',
            name='valor',
            field=models.FloatField(default=0),
        ),
    ]
