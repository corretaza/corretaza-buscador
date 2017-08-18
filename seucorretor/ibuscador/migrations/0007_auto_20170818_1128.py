# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ibuscador', '0006_imovel_valor_iptu'),
    ]

    operations = [
        migrations.AddField(
            model_name='imovel',
            name='destaque_para_portais',
            field=models.BooleanField(default=False, verbose_name='Marca imovel como destaque'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='imovel',
            name='super_destaque_para_portais',
            field=models.BooleanField(default=False, verbose_name='Marca imovel como super destaque'),
            preserve_default=True,
        ),
    ]
