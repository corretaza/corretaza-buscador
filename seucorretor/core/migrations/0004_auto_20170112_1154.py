# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20170112_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interesse',
            name='data_ultima_comunicacao',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='\xdaltima comunica\xe7\xe3o'),
            preserve_default=True,
        ),
    ]
