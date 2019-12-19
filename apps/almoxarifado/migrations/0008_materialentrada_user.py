# Generated by Django 2.2.7 on 2019-12-18 19:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('almoxarifado', '0007_auto_20191218_1548'),
    ]

    operations = [
        migrations.AddField(
            model_name='materialentrada',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='almoxarifado_entradas', to=settings.AUTH_USER_MODEL),
        ),
    ]