# Generated by Django 2.2.7 on 2019-12-03 15:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web_gc', '0002_remove_cadastrotalao_posto'),
    ]

    operations = [
        migrations.AddField(
            model_name='cadastrotalao',
            name='posto',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='talao_posto', to='web_gc.Posto'),
        ),
    ]
