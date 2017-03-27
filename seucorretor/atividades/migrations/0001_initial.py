# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autoatendimento', '0002_auto_20170203_1003'),
    ]

    operations = [
        migrations.CreateModel(
            name='Atividade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ator', models.CharField(default='', max_length=64, verbose_name='Ator', blank=True)),
                ('acao', models.CharField(default='', max_length=64, verbose_name='A\xe7\xe3o', blank=True)),
                ('objeto', models.CharField(default='', max_length=64, verbose_name='Objeto', blank=True)),
                ('detalhe', models.TextField(default='', max_length=1024, verbose_name='Detalhe', blank=True)),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data')),
                ('interesse', models.ForeignKey(verbose_name='interesse', to='autoatendimento.Interesse')),
            ],
            options={
                'ordering': ['data'],
                'verbose_name': 'atividade',
                'verbose_name_plural': 'atividades',
            },
            bases=(models.Model,),
        ),
    ]
