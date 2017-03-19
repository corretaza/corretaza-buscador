# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ibuscador', '0005_condominio_portaria_atualizada_em'),
    ]

    operations = [
        migrations.AddField(
            model_name='imovel',
            name='valor_iptu',
            field=models.DecimalField(default=0.0, verbose_name='Valor IPTU', max_digits=12, decimal_places=2),
            preserve_default=True,
        ),
    ]
