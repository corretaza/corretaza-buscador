# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bairro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=128, verbose_name='Bairro')),
                ('nome_popular', models.CharField(max_length=128, verbose_name='Nome popular', blank=True)),
            ],
            options={
                'ordering': ['regiao', 'nome_popular', 'nome'],
                'verbose_name': 'Bairro',
                'verbose_name_plural': 'Bairros',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cidade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=128, verbose_name='Nome da cidade')),
                ('nome_abreviado', models.CharField(default='', max_length=64, verbose_name='Abrevia\xe7\xe3o', blank=True)),
            ],
            options={
                'verbose_name': 'Cidade',
                'verbose_name_plural': 'Cidades',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Regiao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=64, verbose_name='Nome da regi\xe3o')),
                ('cidade', models.ForeignKey(verbose_name='Cidade', to='cidades.Cidade')),
            ],
            options={
                'verbose_name': 'Regi\xe3o',
                'verbose_name_plural': 'Regi\xf5es',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='bairro',
            name='cidade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Cidade', blank=True, to='cidades.Cidade', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bairro',
            name='regiao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Regi\xe3o', blank=True, to='cidades.Regiao', null=True),
            preserve_default=True,
        ),
    ]
