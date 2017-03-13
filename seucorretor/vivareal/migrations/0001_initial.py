# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ibuscador', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item', models.CharField(max_length=512)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PropertyList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('listing_id', models.CharField(max_length=32)),
                ('transaction_type', models.CharField(max_length=16)),
                ('featured', models.BooleanField(default=False)),
                ('property_type', models.CharField(max_length=128, blank=True)),
                ('description', models.TextField(max_length=1024, blank=True)),
                ('list_price', models.IntegerField(default=0, blank=True)),
                ('rental_price', models.IntegerField(default=0, blank=True)),
                ('property_administration_fee', models.IntegerField(default=0, blank=True)),
                ('bedrooms', models.IntegerField(default=0, blank=True)),
                ('bathrooms', models.IntegerField(default=0, blank=True)),
                ('garage', models.IntegerField(default=0, blank=True)),
                ('constructed_area', models.DecimalField(default=0.0, max_digits=12, decimal_places=2)),
                ('country', models.CharField(max_length=64, blank=True)),
                ('state', models.CharField(max_length=8, blank=True)),
                ('city', models.CharField(max_length=64, blank=True)),
                ('neighborhood', models.CharField(max_length=128, blank=True)),
                ('postal_code', models.CharField(max_length=16, blank=True)),
                ('archived', models.BooleanField(default=False)),
                ('new', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='media',
            name='property_list',
            field=models.ForeignKey(verbose_name='property', to='vivareal.PropertyList'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='ImovelVivaReal',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('ibuscador.imovel',),
        ),
    ]
