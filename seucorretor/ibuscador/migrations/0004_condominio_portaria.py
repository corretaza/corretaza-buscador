# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ibuscador', '0003_imovel_tipo_varanda'),
    ]

    operations = [
        migrations.AddField(
            model_name='condominio',
            name='portaria',
            field=models.CharField(default='', max_length=16, blank=True, choices=[('', '-'), ('semportaria', 'Sem Portaria'), ('semporteiro', 'Sem Porteiro'), ('24h', 'Portaria 24h'), ('eletronica', 'Eletr\xf4nica'), ('hcomercial', 'Em Hor\xe1rio Comercial'), ('cameras', 'Com Cameras')]),
            preserve_default=True,
        ),
    ]
