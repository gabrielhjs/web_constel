# Generated by Django 3.1.7 on 2021-06-21 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talao', '0003_auto_20210621_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entregavale',
            name='data',
            field=models.DateTimeField(),
        ),
    ]