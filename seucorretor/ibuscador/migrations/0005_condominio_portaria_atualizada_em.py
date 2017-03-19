# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ibuscador', '0004_condominio_portaria'),
    ]

    operations = [
        migrations.AddField(
            model_name='condominio',
            name='portaria_atualizada_em',
            field=models.DateTimeField(null=True, verbose_name='Data da atualiza\xe7\xe3o da portaria', blank=True),
            preserve_default=True,
        ),
    ]
