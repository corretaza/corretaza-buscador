# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    state_operations = [
        migrations.RemoveField(
            model_name='interesse',
            name='bairros',
        ),
        migrations.RemoveField(
            model_name='interesse',
            name='cidade',
        ),
        migrations.RemoveField(
            model_name='interesse',
            name='cliente',
        ),
        migrations.RemoveField(
            model_name='interesse',
            name='corretor',
        ),
        migrations.RemoveField(
            model_name='mensagem',
            name='de',
        ),
        migrations.RemoveField(
            model_name='mensagem',
            name='interesse',
        ),
        migrations.RemoveField(
            model_name='mensagem',
            name='para',
        ),
        migrations.DeleteModel(
            name='Mensagem',
        ),
        migrations.RemoveField(
            model_name='opcaoparavisita',
            name='interesse',
        ),
        migrations.DeleteModel(
            name='Interesse',
        ),
        migrations.DeleteModel(
            name='OpcaoParaVisita',
        ),
        migrations.DeleteModel(
            name='Solicitation',
        ),
        migrations.DeleteModel(
            name='Cliente',
        ),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]
