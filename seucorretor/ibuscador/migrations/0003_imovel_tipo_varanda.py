# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ibuscador', '0002_imovel_nao_exportar_para_portais'),
    ]

    operations = [
        migrations.AddField(
            model_name='imovel',
            name='tipo_varanda',
            field=models.CharField(default='', max_length=16, blank=True, choices=[('', '-'), ('sem', 'Sem Varanda/Sacada'), ('varanda', 'Com Varanda'), ('varandaG', 'Com Varanda Gourmet'), ('sacada', 'Com Sacada'), ('terraco', 'Com Terra\xe7o'), ('terracoG', 'Com Terra\xe7o Gourmet')]),
            preserve_default=True,
        ),
    ]
