# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ibuscador', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ZapPreferences',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('qtd_imoveis_para_exportacao', models.PositiveIntegerField(default=100, verbose_name='Quantidade de im\xf3veis para exportar', blank=True)),
            ],
            options={
                'verbose_name': 'ZapPreferences',
                'verbose_name_plural': 'ZapPreferences',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImovelWeb',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('ibuscador.imovel',),
        ),
        migrations.CreateModel(
            name='ImovelZapImovel',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('ibuscador.imovel',),
        ),
    ]
