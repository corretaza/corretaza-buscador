# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.crypto
import django.db.models.deletion
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cidades', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Colaborador',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cep', models.CharField(max_length=16, verbose_name='CEP', blank=True)),
                ('logradouro', models.CharField(default='', max_length=256, verbose_name='Logradouro', blank=True)),
                ('numero', models.CharField(max_length=16, verbose_name='N\xfamero', blank=True)),
                ('complemento', models.CharField(default='', help_text='Nro. apto, Andar e Bloco', max_length=64, verbose_name='Complemento', blank=True)),
                ('slug', models.SlugField(default=django.utils.crypto.get_random_string)),
                ('is_ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('nome', models.CharField(max_length=128, verbose_name='nome')),
                ('email', models.EmailField(default='', max_length=128, verbose_name='e-mail')),
                ('fone', models.CharField(default='', max_length=32, verbose_name='fone')),
                ('fone2', models.CharField(max_length=32, verbose_name='fone 2', blank=True)),
                ('fone3', models.CharField(max_length=32, verbose_name='fone 3', blank=True)),
                ('fone_detalhe', models.CharField(default='', max_length=32, verbose_name='Operadora', blank=True)),
                ('fone2_detalhe', models.CharField(default='', max_length=32, verbose_name='Operadora', blank=True)),
                ('fone3_detalhe', models.CharField(default='', max_length=32, verbose_name='Operadora', blank=True)),
                ('whatsapp', models.CharField(default='', max_length=32, verbose_name='WhatsApp', blank=True)),
                ('foto', models.ImageField(default='', upload_to='corretor_foto/%Y/%m/%d', verbose_name='foto', blank=True)),
                (b'foto_cropping', image_cropping.fields.ImageRatioField('foto', '296x324', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='foto cropping')),
                ('cpf', models.CharField(default='', max_length=16, verbose_name='CPF', blank=True)),
                ('rg', models.CharField(default='', max_length=16, verbose_name='RG', blank=True)),
                ('data_nascimento', models.DateField(null=True, blank=True)),
                ('data_admissao', models.DateField(null=True, blank=True)),
                ('data_rescisao', models.DateField(null=True, blank=True)),
                ('banco_ag_cc', models.CharField(default='', max_length=128, verbose_name='Banco, Ag e CC', blank=True)),
                ('email_particular', models.EmailField(default='', max_length=128, verbose_name='e-mail particular', blank=True)),
                ('fone_particular', models.CharField(default='', max_length=32, verbose_name='fone particular', blank=True)),
                ('pode_alterar_imovel', models.BooleanField(default=True)),
                ('creci', models.CharField(default='', max_length=16, verbose_name='CRECI')),
                ('comprar_contador', models.BigIntegerField(default=1, verbose_name='comprar cont.')),
                ('alugar_contador', models.BigIntegerField(default=1, verbose_name='alugar cont.')),
                ('pausado', models.BooleanField(default=False, verbose_name='Pausado para atendimento')),
                ('bairro', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Bairro', blank=True, to='cidades.Bairro', null=True)),
                ('cidade', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Cidade', blank=True, to='cidades.Cidade', null=True)),
                ('regiao', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Regi\xe3o', blank=True, to='cidades.Regiao', null=True)),
            ],
            options={
                'ordering': ['-is_ativo', 'nome'],
                'verbose_name': 'colaborador',
                'verbose_name_plural': 'colaboradores',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImobiliariaPreferences',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(default='', max_length=128, verbose_name='Nome', blank=True)),
                ('cep', models.CharField(max_length=16, verbose_name='CEP', blank=True)),
                ('logradouro', models.CharField(default='', max_length=256, verbose_name='Logradouro', blank=True)),
                ('numero', models.CharField(max_length=16, verbose_name='N\xfamero', blank=True)),
                ('complemento', models.CharField(default='', max_length=64, verbose_name='Complemento', blank=True)),
                ('bairro', models.CharField(default='', max_length=128, verbose_name='Bairro', blank=True)),
                ('cidade', models.CharField(default='', max_length=128, verbose_name='Cidade', blank=True)),
                ('fone1', models.CharField(max_length=32, verbose_name='fone 1', blank=True)),
                ('fone2', models.CharField(max_length=32, verbose_name='fone 2', blank=True)),
                ('email_contato', models.EmailField(max_length=128, verbose_name='e-mail contato', blank=True)),
                ('site_url', models.CharField(max_length=128, verbose_name='Site link', blank=True)),
                ('horario_funcionamento', models.CharField(default='', max_length=128, verbose_name='Hor\xe1rio funcionamento', blank=True)),
                ('email_inbount_mensagem', models.EmailField(max_length=128, verbose_name='e-mail inbount mensagem', blank=True)),
                ('email_notificacao_estatisticas', models.CharField(max_length=512, verbose_name='Email notificacao estatisticas', blank=True)),
                ('logo', models.ImageField(default='', upload_to='imobiliaria/%Y/%m/%d', verbose_name='logo', blank=True)),
                (b'logo_cropping', image_cropping.fields.ImageRatioField('logo', '340x210', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='logo cropping')),
            ],
            options={
                'verbose_name': 'Prefer\xeancia',
                'verbose_name_plural': 'Prefer\xeancias',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Corretor',
            fields=[
            ],
            options={
                'ordering': ['-is_ativo', 'nome'],
                'verbose_name': 'corretor',
                'proxy': True,
                'verbose_name_plural': 'corretores',
            },
            bases=('imobiliaria.colaborador',),
        ),
    ]
