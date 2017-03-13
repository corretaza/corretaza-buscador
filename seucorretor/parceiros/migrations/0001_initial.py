# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Parceiro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('exibir', models.BooleanField(default=True, verbose_name='Exibir')),
                ('titulo', models.CharField(default='', max_length=128, verbose_name='Titulo', blank=True)),
                ('link', models.URLField(default='', verbose_name='Link', blank=True)),
                ('imagem', models.ImageField(default='', upload_to='parceiro_imagem/%Y/%m', verbose_name='imagem', blank=True)),
                (b'imagem_cropping', image_cropping.fields.ImageRatioField('imagem', '864x764', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=True, adapt_rotation=False, help_text=None, verbose_name='imagem cropping')),
            ],
            options={
                'verbose_name': 'Parceiro',
                'verbose_name_plural': 'Parceiros',
            },
            bases=(models.Model,),
        ),
    ]
