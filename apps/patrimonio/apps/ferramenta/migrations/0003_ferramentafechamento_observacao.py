# Generated by Django 3.0.7 on 2020-08-25 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ferramenta', '0002_ferramentafechamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='ferramentafechamento',
            name='observacao',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='Observação'),
        ),
    ]