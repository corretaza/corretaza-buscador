# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('imobiliaria', '__first__'),
        ('cidades', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AreaDeLazer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descricao', models.CharField(unique=True, max_length=128, verbose_name='\xc1rea de lazer')),
                ('tag_vivareal', models.CharField(default='', max_length=64, verbose_name='Tag vivareal', blank=True)),
            ],
            options={
                'ordering': ('descricao',),
                'verbose_name': '\xc1rea de lazer',
                'verbose_name_plural': '\xc1reas de lazer',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BairroComImoveis',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo_imovel', models.CharField(default='', max_length=16, choices=[('apartamento', 'Apartamento'), ('casa', 'Casa'), ('terreno', 'Terreno'), ('areaurbana', '\xc1rea urbana'), ('chacara', 'Ch\xe1cara/S\xedtio'), ('loja', 'Loja/Ponto'), ('sala', 'Sala/Consult\xf3rio'), ('galpao', 'Galp\xe3o/Dep\xf3sito'), ('edificio', 'Edif\xedcio/Pr\xe9dio')])),
                ('contador_venda', models.PositiveSmallIntegerField(default=0)),
                ('contador_locacao', models.PositiveSmallIntegerField(default=0)),
                ('bairro', models.ForeignKey(verbose_name='Bairro', to='cidades.Bairro')),
                ('cidade', models.ForeignKey(verbose_name='Cidade', blank=True, to='cidades.Cidade', null=True)),
                ('regiao', models.ForeignKey(verbose_name='Regi\xe3o', blank=True, to='cidades.Regiao', null=True)),
            ],
            options={
                'verbose_name': 'Bairro com im\xf3veis',
                'verbose_name_plural': 'Bairros com im\xf3veis',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Condominio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cep', models.CharField(max_length=16, verbose_name='CEP', blank=True)),
                ('logradouro', models.CharField(default='', max_length=256, verbose_name='Logradouro', blank=True)),
                ('numero', models.CharField(max_length=16, verbose_name='N\xfamero', blank=True)),
                ('complemento', models.CharField(default='', help_text='Nro. apto, Andar e Bloco', max_length=64, verbose_name='Complemento', blank=True)),
                ('data_cadastro', models.DateTimeField(auto_now_add=True, verbose_name='data cadastro')),
                ('atualizado_em', models.DateTimeField(auto_now=True, verbose_name='atualizado em')),
                ('nome', models.CharField(unique=True, max_length=128, verbose_name='Nome do condom\xednio')),
                ('blocos', models.PositiveSmallIntegerField(default=0, verbose_name='Qtd de blocos', blank=True)),
                ('andares', models.PositiveSmallIntegerField(default=0, verbose_name='N\xfamero de andares', blank=True)),
                ('apto_por_andar', models.PositiveSmallIntegerField(default=0, verbose_name='Apto por andar', blank=True)),
                ('tem_elevador', models.BooleanField(default=False, verbose_name='Tem elevador')),
                ('construtora', models.CharField(max_length=256, verbose_name='Nome da construtora', blank=True)),
                ('ano_construcao', models.PositiveIntegerField(default=0, verbose_name='Ano constru\xe7\xe3o', blank=True)),
                ('contato_portaria', models.CharField(default='', max_length=128, verbose_name='Contato portaria', blank=True)),
                ('contato_zelador', models.CharField(default='', max_length=128, verbose_name='Contato zelador', blank=True)),
                ('contato_administradora', models.CharField(default='', max_length=128, verbose_name='Contato Administradora', blank=True)),
                ('regras_mudanca', models.CharField(default='', max_length=128, verbose_name='Regras para mudan\xe7as', blank=True)),
                ('areadelazer_condominio', models.ManyToManyField(to='ibuscador.AreaDeLazer', blank=True)),
                ('bairro', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Bairro', blank=True, to='cidades.Bairro', null=True)),
                ('cidade', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Cidade', blank=True, to='cidades.Cidade', null=True)),
                ('regiao', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Regi\xe3o', blank=True, to='cidades.Regiao', null=True)),
            ],
            options={
                'ordering': ('nome',),
                'verbose_name': 'Condom\xednio',
                'verbose_name_plural': 'Condom\xednios',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DescricaoComodo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo_imovel', models.CharField(blank=True, max_length=16, null=True, verbose_name='Tipo do im\xf3vel', choices=[('apartamento', 'Apartamento'), ('casa', 'Casa'), ('terreno', 'Terreno'), ('areaurbana', '\xc1rea urbana'), ('chacara', 'Ch\xe1cara/S\xedtio'), ('loja', 'Loja/Ponto'), ('sala', 'Sala/Consult\xf3rio'), ('galpao', 'Galp\xe3o/Dep\xf3sito'), ('edificio', 'Edif\xedcio/Pr\xe9dio')])),
                ('descricao', models.CharField(max_length=255, null=True, verbose_name='descri\xe7\xe3o', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DescricaoImovel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo_imovel', models.CharField(blank=True, max_length=16, null=True, verbose_name='Tipo do im\xf3vel', choices=[('apartamento', 'Apartamento'), ('casa', 'Casa'), ('terreno', 'Terreno'), ('areaurbana', '\xc1rea urbana'), ('chacara', 'Ch\xe1cara/S\xedtio'), ('loja', 'Loja/Ponto'), ('sala', 'Sala/Consult\xf3rio'), ('galpao', 'Galp\xe3o/Dep\xf3sito'), ('edificio', 'Edif\xedcio/Pr\xe9dio')])),
                ('descricao', models.CharField(max_length=255, null=True, verbose_name='descri\xe7\xe3o', blank=True)),
            ],
            options={
                'ordering': ['descricao'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FormaDePagamento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descricao', models.CharField(unique=True, max_length=64, verbose_name='Forma de pagamento')),
            ],
            options={
                'ordering': ('descricao',),
                'verbose_name': 'Forma de Pagamento',
                'verbose_name_plural': 'Formas de Pagamento',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Foto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descricao', models.CharField(max_length=255, null=True, verbose_name='descri\xe7\xe3o', blank=True)),
                ('picture', models.ImageField(default='', upload_to='imovel_fotos/%Y/%m', verbose_name='picture', blank=True)),
                (b'picture_cropping', image_cropping.fields.ImageRatioField('picture', '1024x632', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=True, adapt_rotation=False, help_text=None, verbose_name='picture cropping')),
                ('ordem', models.IntegerField(default=1, null=True, blank=True)),
                ('eh_principal', models.BooleanField(default=False, verbose_name='Foto Principal')),
            ],
            options={
                'verbose_name': 'foto',
                'verbose_name_plural': 'fotos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricoDeImovel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.DateTimeField()),
                ('conteudo', models.CharField(default='', max_length=1024, verbose_name='conteudo')),
            ],
            options={
                'ordering': ['-data'],
                'verbose_name': 'historico',
                'verbose_name_plural': 'historicos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Imovel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cep', models.CharField(max_length=16, verbose_name='CEP', blank=True)),
                ('logradouro', models.CharField(default='', max_length=256, verbose_name='Logradouro', blank=True)),
                ('numero', models.CharField(max_length=16, verbose_name='N\xfamero', blank=True)),
                ('complemento', models.CharField(default='', help_text='Nro. apto, Andar e Bloco', max_length=64, verbose_name='Complemento', blank=True)),
                ('slug', models.SlugField(default='', max_length=128, blank=True)),
                ('data_cadastro', models.DateTimeField(auto_now_add=True, verbose_name='data cadastro')),
                ('atualizado_em', models.DateTimeField(auto_now=True, verbose_name='atualizado em')),
                ('status', models.CharField(default='novo', max_length=16, choices=[('novo', 'Novo'), ('publicado', 'Publicado'), ('arquivado', 'Arquivado')])),
                ('imovel_ref', models.CharField(default='', max_length=32, verbose_name='Refer\xeancia')),
                ('eh_para_locacao', models.BooleanField(default=False, verbose_name='Para loca\xe7\xe3o')),
                ('valor_locacao', models.DecimalField(default=0.0, verbose_name='Valor loca\xe7\xe3o', max_digits=12, decimal_places=2)),
                ('eh_para_venda', models.BooleanField(default=False, verbose_name='Para venda')),
                ('valor_venda', models.DecimalField(default=0.0, verbose_name='Valor venda', max_digits=12, decimal_places=2)),
                ('valor_condominio', models.DecimalField(default=0.0, verbose_name='Valor condom\xednio', max_digits=12, decimal_places=2)),
                ('tipo_imovel', models.CharField(max_length=16, verbose_name='Tipo do im\xf3vel', choices=[('apartamento', 'Apartamento'), ('casa', 'Casa'), ('terreno', 'Terreno'), ('areaurbana', '\xc1rea urbana'), ('chacara', 'Ch\xe1cara/S\xedtio'), ('loja', 'Loja/Ponto'), ('sala', 'Sala/Consult\xf3rio'), ('galpao', 'Galp\xe3o/Dep\xf3sito'), ('edificio', 'Edif\xedcio/Pr\xe9dio')])),
                ('eh_apto_duplex', models.BooleanField(default=False, verbose_name='Duplex')),
                ('eh_apto_triplex', models.BooleanField(default=False, verbose_name='Triplex')),
                ('eh_apto_cobertura', models.BooleanField(default=False, verbose_name='Cobertura')),
                ('eh_casa_terrea', models.BooleanField(default=False, verbose_name='Terrea')),
                ('eh_casa_edicula', models.BooleanField(default=False, verbose_name='Ed\xedcula')),
                ('eh_casa_sobreloja', models.BooleanField(default=False, verbose_name='Sobreloja')),
                ('eh_casa_sobrado', models.BooleanField(default=False, verbose_name='Sobrado')),
                ('eh_casa_geminada', models.BooleanField(default=False, verbose_name='Geminada')),
                ('eh_kitnet', models.BooleanField(default=False, verbose_name='Kitnet')),
                ('eh_imovel_novo', models.BooleanField(default=False, verbose_name='Im\xf3vel novo')),
                ('eh_comercial', models.BooleanField(default=False, verbose_name='Im\xf3vel comercial')),
                ('dormitorios', models.PositiveSmallIntegerField(default=0, verbose_name='Nro. Dormit\xf3rios', blank=True)),
                ('banheiros', models.PositiveSmallIntegerField(default=0, verbose_name='Nro. Banheiros', blank=True)),
                ('suites', models.PositiveSmallIntegerField(default=0, verbose_name='Nro. Su\xedtes', blank=True)),
                ('vagas_garagem', models.PositiveSmallIntegerField(default=0, verbose_name='Vagas Garagem', blank=True)),
                ('area_construida', models.PositiveIntegerField(default=0, verbose_name='\xc1rea Constru\xedda', blank=True)),
                ('area_terreno', models.PositiveIntegerField(default=0, verbose_name='\xc1rea Terreno', blank=True)),
                ('dimensoes_terreno', models.CharField(default='', max_length=64, verbose_name='Dimens\xf5es Terreno', blank=True)),
                ('descricao_imovel', models.TextField(default='', verbose_name='Descri\xe7\xe3o do im\xf3vel', blank=True)),
                ('descricao_comodos', models.TextField(default='', verbose_name='Descri\xe7\xe3o c\xf4modos', blank=True)),
                ('esta_ocupado', models.BooleanField(default=False, verbose_name='Ocupado')),
                ('esta_mobiliado', models.BooleanField(default=False, verbose_name='Mobiliado')),
                ('esta_com_placa', models.BooleanField(default=False, verbose_name='Com placa')),
                ('local_chave', models.CharField(default='proprietario', max_length=16, choices=[('imobiliaria', 'Imobiliaria'), ('portaria', 'Portaria'), ('proprietario', 'Propriet\xe1rio'), ('outro', 'Outro')])),
                ('local_chave_observacao', models.CharField(default='', max_length=128, verbose_name='Local da chave observa\xe7\xe3o', blank=True)),
                ('observacoes_internas', models.TextField(default='', verbose_name='Observa\xe7\xf5es internas', blank=True)),
                ('outra_forma_de_pagamento', models.CharField(default='', max_length=128, verbose_name='Outras formas de pagamentos', blank=True)),
                ('indicado_por', models.CharField(default='', max_length=128, verbose_name='Indicado por', blank=True)),
                ('areadelazer_imovel', models.ManyToManyField(to='ibuscador.AreaDeLazer', verbose_name='do im\xf3vel', blank=True)),
                ('bairro', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Bairro', blank=True, to='cidades.Bairro', null=True)),
                ('cidade', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Cidade', blank=True, to='cidades.Cidade', null=True)),
                ('condominio', models.ForeignKey(verbose_name='Condom\xednio', blank=True, to='ibuscador.Condominio', null=True)),
                ('corretores', models.ManyToManyField(to='imobiliaria.Corretor', verbose_name='Corretores', blank=True)),
                ('forma_de_pagamentos', models.ManyToManyField(to='ibuscador.FormaDePagamento', blank=True)),
                ('foto_principal', models.ForeignKey(related_name='fotos', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Foto Principal', blank=True, to='ibuscador.Foto', null=True)),
                ('proprietario', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Propriet\xe1rio', to='crm.Proprietario', null=True)),
                ('regiao', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Regi\xe3o', blank=True, to='cidades.Regiao', null=True)),
            ],
            options={
                'get_latest_by': 'data_cadastro',
                'verbose_name': 'Im\xf3vel',
                'verbose_name_plural': 'Im\xf3veis',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='historicodeimovel',
            name='imovel',
            field=models.ForeignKey(related_name='historicoalteracoes', verbose_name='Imovel', to='ibuscador.Imovel'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicodeimovel',
            name='usuario',
            field=models.ForeignKey(related_name='usuario', verbose_name='Usuario', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='foto',
            name='imovel',
            field=models.ForeignKey(verbose_name='Imovel', to='ibuscador.Imovel'),
            preserve_default=True,
        ),
    ]
