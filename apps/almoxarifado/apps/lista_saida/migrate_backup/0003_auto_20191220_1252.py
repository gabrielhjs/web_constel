# Generated by Django 2.2.7 on 2019-12-20 15:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lista_saida', '0002_auto_20191220_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lista',
            name='user_to',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='lista_retirada', to=settings.AUTH_USER_MODEL),
        ),
    ]