# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HitCount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified')),
                ('url', models.CharField(max_length=2000, verbose_name='URL')),
                ('hits', models.PositiveIntegerField(default=0, verbose_name='Hits')),
                ('year', models.PositiveIntegerField(default=0, verbose_name='Ano')),
                ('month', models.PositiveIntegerField(default=0, verbose_name='Mes')),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-created', '-modified'),
                'get_latest_by': 'created',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HitDataCount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.PositiveIntegerField(default=0, verbose_name='Ano')),
                ('month', models.PositiveIntegerField(default=0, verbose_name='Mes')),
                ('period', models.CharField(default='Total', max_length=32, verbose_name='Periodo')),
                ('data', models.CharField(max_length=512, verbose_name='Dado')),
                ('hits', models.PositiveIntegerField(default=0, verbose_name='Hits')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified')),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-id',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PageViewCount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('url', models.CharField(max_length=2000, verbose_name='URL')),
            ],
            options={
                'ordering': ('-id',),
                'get_latest_by': 'created',
            },
            bases=(models.Model,),
        ),
    ]
