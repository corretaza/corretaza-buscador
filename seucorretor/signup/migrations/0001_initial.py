# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('imobiliaria', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account_type', models.CharField(default='estagiario', max_length=32, blank=True, choices=[('gerente', 'Gerente'), ('corretor', 'Corretor'), ('estagiario', 'Estagiario')])),
                ('corretor', models.ForeignKey(verbose_name='corretor', blank=True, to='imobiliaria.Colaborador', null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Users Profile',
            },
            bases=(models.Model,),
        ),
    ]
