# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20170111_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interesse',
            name='data_ultima_comunicacao',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 12, 13, 48, 37, 935202, tzinfo=utc), verbose_name='\xdaltima comunica\xe7\xe3o'),
            preserve_default=True,
        ),
    ]
