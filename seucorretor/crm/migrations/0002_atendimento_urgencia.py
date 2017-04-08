# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='atendimento',
            name='urgencia',
            field=models.CharField(default='9', max_length=2, verbose_name='Urgencia', choices=[('0', 'Muito urgente, preciso achar um im\xf3vel em menos de 1 semana/mes'), ('1', 'Urgente, preciso achar um im\xf3vel dentro 3 meses'), ('2', 'N\xe3o urgente, estou pesquisando para comprar daqui 6 meses ou 1 ano'), ('3', 'Investidor, quero o melhor custo/benef\xedcio'), ('9', 'N\xe3o informado')]),
            preserve_default=True,
        ),
    ]
