# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autoatendimento', '0003_auto_20170203_1017'),
    ]

    operations = [
        migrations.CreateModel(
            name='InteresseEstatistica',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('autoatendimento.interesse',),
        ),
    ]
