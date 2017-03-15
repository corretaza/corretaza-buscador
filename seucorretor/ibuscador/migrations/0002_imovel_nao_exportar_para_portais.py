# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ibuscador', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='imovel',
            name='nao_exportar_para_portais',
            field=models.BooleanField(default=False, verbose_name='N\xe3o exportar para portais imobiliarios'),
            preserve_default=True,
        ),
    ]
