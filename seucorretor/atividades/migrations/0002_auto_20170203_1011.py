# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('atividades', '0001_initial'),
        ('autoatendimento', '0002_auto_20170203_1003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atividade',
            name='interesse',
            field=models.ForeignKey(verbose_name='interesse', to='autoatendimento.Interesse'),
            preserve_default=True,
        ),
    ]
