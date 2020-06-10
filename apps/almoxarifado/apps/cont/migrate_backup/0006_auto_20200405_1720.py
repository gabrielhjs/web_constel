# Generated by Django 2.2.7 on 2020-04-05 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cont', '0005_ontentradahistorico'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ontaplicado',
            old_name='ont',
            new_name='serial',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='nome',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='sinal_olt',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='sinal_ont',
        ),
        migrations.AddField(
            model_name='cliente',
            name='estado_link',
            field=models.CharField(default='vazio', max_length=255),
        ),
        migrations.AddField(
            model_name='cliente',
            name='nivel_olt',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='cliente',
            name='nivel_olt_tx',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='cliente',
            name='nivel_ont',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='cliente',
            name='porta',
            field=models.CharField(default='vazio', max_length=255),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='contrato',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ontaplicado',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='aplicado_cliente', to='cont.Cliente'),
        ),
    ]