# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20160624_1009'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grafico',
            name='teste',
        ),
        migrations.RemoveField(
            model_name='testevelocidadevariavel',
            name='testeVV_quantidade_velocidade',
        ),
        migrations.AlterField(
            model_name='testevelocidadefixa',
            name='testeVF_velocidade',
            field=models.FloatField(validators=[django.core.validators.MaxValueValidator(225), django.core.validators.MinValueValidator(1)], verbose_name='Velocidade do Motor', default=5, null=True),
        ),
        migrations.DeleteModel(
            name='Grafico',
        ),
    ]
