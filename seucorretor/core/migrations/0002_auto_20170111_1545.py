# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interesse',
            name='data_ultima_comunicacao',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 11, 17, 45, 44, 734676, tzinfo=utc), verbose_name='\xdaltima comunica\xe7\xe3o'),
            preserve_default=True,
        ),
    ]
