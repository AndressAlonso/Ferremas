# Generated by Django 5.0.6 on 2025-05-16 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_perfilusuario_direccion'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfilusuario',
            name='latitud',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='perfilusuario',
            name='longitud',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
