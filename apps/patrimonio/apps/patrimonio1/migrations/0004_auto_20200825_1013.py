# Generated by Django 3.0.7 on 2020-08-25 10:13

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('patrimonio1', '0003_auto_20200824_1208'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PatrimonioEntrada',
            new_name='PatrimonioEntrada1',
        ),
    ]