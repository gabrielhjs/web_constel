# Generated by Django 3.0.7 on 2021-03-14 20:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Km',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('km_initial', models.FloatField()),
                ('km_final', models.FloatField(null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='km_users+', to=settings.AUTH_USER_MODEL)),
                ('user_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="{'class': 'km', 'model_name': 'km', 'app_label': 'km'}(class)s_users_to+", to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
