# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.crypto
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('imobiliaria', '0001_initial'),
        ('crm', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cidades', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interesse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(default=django.utils.crypto.get_random_string)),
                ('status', models.CharField(default='0', max_length=4, verbose_name='status', choices=[('0', 'Novo'), ('1', 'Perfil'), ('2', 'Buscando Im\xf3vel'), ('3', 'Aguardando An\xe1lise'), ('4', 'Visita'), ('5', 'Proposta'), ('6', 'Contrato'), ('7', 'Pausado'), ('9', 'Finalizado')])),
                ('data_envio_contato', models.DateTimeField(default=datetime.datetime.now)),
                ('data_contato', models.DateTimeField(auto_now_add=True)),
                ('tipo_interesse', models.CharField(max_length=16, verbose_name='tipo de interesse', choices=[('comprar', 'Comprar'), ('alugar', 'Alugar')])),
                ('tipo_imovel', models.CharField(blank=True, max_length=16, verbose_name='tipo do im\xf3vel', choices=[('apartamento', 'Apartamento'), ('casa', 'Casa'), ('terreno', 'Terreno'), ('areaurbana', '\xc1rea urbana'), ('chacara', 'Ch\xe1cara/S\xedtio'), ('loja', 'Loja/Ponto'), ('sala', 'Sala/Consult\xf3rio'), ('galpao', 'Galp\xe3o/Dep\xf3sito'), ('edificio', 'Edif\xedcio/Pr\xe9dio')])),
                ('numero_dormitorios', models.IntegerField(default=1, verbose_name='Nro. M\xednimo Dormit\xf3rios', blank=True)),
                ('numero_vagas', models.IntegerField(default=1, verbose_name='M\xednimo Vagas', blank=True)),
                ('area_construida', models.IntegerField(default=30, verbose_name='\xc1rea M\xedn. Constru\xedda', blank=True)),
                ('is_andar_baixo', models.BooleanField(default=True, verbose_name='Andar Baixo')),
                ('is_andar_medio', models.BooleanField(default=True, verbose_name='Andar M\xe9dio')),
                ('is_andar_alto', models.BooleanField(default=True, verbose_name='Andar Alto')),
                ('is_terreo', models.BooleanField(default=True, verbose_name='T\xe9rreo')),
                ('is_sobrado', models.BooleanField(default=True, verbose_name='Sobrado')),
                ('eh_comercial', models.BooleanField(default=False, verbose_name='Im\xf3vel comercial')),
                ('nota_bairro', models.CharField(default='', max_length=128, verbose_name='Notas sobre bairros', blank=True)),
                ('urgencia', models.CharField(default='9', max_length=8, verbose_name='urg\xeancia', choices=[('0', 'Muito urgente'), ('1', 'Urgente'), ('2', 'N\xe3o urgente'), ('9', ' --- ')])),
                ('valor_min', models.DecimalField(default=0.0, verbose_name='valor min.', max_digits=12, decimal_places=2)),
                ('valor', models.DecimalField(default=0.0, verbose_name='Valor max.', max_digits=12, decimal_places=2)),
                ('informacao_inicial', models.CharField(default='', help_text='Entre com o conte\xfado do email ou da conversa via fone', max_length=1024, verbose_name='informa\xe7\xe3o inicial', blank=True)),
                ('imovel_ref_inicial', models.CharField(default='', max_length=32, verbose_name='refer\xeancias', blank=True)),
                ('mais_informacoes', models.CharField(max_length=512, verbose_name='mais informa\xe7\xf5es', blank=True)),
                ('criado_via', models.CharField(default='', max_length=32, verbose_name='Contado vindo via', blank=True, choices=[('vivareal', 'VivaReal'), ('zap', 'Zap'), ('imovelweb', 'Imovel Web'), ('placa', 'Placa'), ('indicacao', 'Indica\xe7\xe3o'), ('site', 'Site'), ('fone', 'Fone'), ('email', 'Email'), ('outros', 'Outros')])),
                ('is_criado_via_corretor', models.BooleanField(default=False)),
                ('nota', models.CharField(default='', max_length=512, verbose_name='Nota do Corretor', blank=True)),
                ('data_ultima_comunicacao', models.DateTimeField(default=datetime.datetime.now, verbose_name='\xdaltima comunica\xe7\xe3o')),
                ('is_pendente_responder_mensagem', models.BooleanField(default=False)),
                ('is_pendente_avisar_sobre_nova_ref', models.BooleanField(default=False)),
                ('is_permuta', models.BooleanField(default=False, verbose_name='Quer permuta')),
                ('is_imovel_novo', models.BooleanField(default=False, verbose_name='Quer imovel novo')),
                ('atende_ligacoes', models.BooleanField(default=True, verbose_name='Esta atendendo liga\xe7\xf5es')),
                ('sem_imoveis_para_perfil', models.BooleanField(default=False, verbose_name='Sem im\xf3veis para o perfil')),
                ('tipo_finalizacao', models.CharField(default='outro', max_length=16, verbose_name='Qual \xe9 o melhor motivo para finalizar este atendimento?', choices=[('sucesso', 'Im\xf3vel vendido/alugado com sucesso!'), ('nao_retorna', 'Cliente n\xe3o retorna contato ou sem interesse'), ('desistiu', 'Desistiu do im\xf3vel ou vai dar um tempo'), ('sem_imovel', 'N\xe3o foi poss\xedvel localizar im\xf3vel para o perfil'), ('negociando_outro', 'J\xe1 achou ou esta negociando com outra imobiliaria'), ('engano', 'Atendimento foi cadastrado por engano'), ('outro', 'Outro')])),
                ('data_perfil', models.DateTimeField(null=True, verbose_name='data perfil', blank=True)),
                ('data_finalizacao', models.DateTimeField(null=True, verbose_name='data finaliza\xe7\xe3o', blank=True)),
                ('data_proposta', models.DateTimeField(null=True, verbose_name='data proposta', blank=True)),
                ('data_contrato', models.DateTimeField(null=True, verbose_name='data contrato', blank=True)),
                ('cancelado_pelo_cliente', models.BooleanField(default=False)),
                ('cancelamento_motivo', models.CharField(default='', max_length=16, verbose_name='Qual \xe9 o motivo para voc\xea CANCELAR o nosso atendimento?', blank=True, choices=[('fechou_neg', 'J\xe1 achei um im\xf3vel'), ('poucasopcoes', 'N\xe3o recebi op\xe7\xf5es de im\xf3veis do meu interesse'), ('atend_ruim', 'Atendimento ruim ou muito demorado'), ('muito_email', 'Muitos emails que n\xe3o tenho interesse'), ('corretor', 'N\xe3o gostei do corretor'), ('engano', 'Me cadastrei por engano e n\xe3o quero um im\xf3vel'), ('outro', 'Outro'), ('nao_cancelar', 'Quero continuar o atendimento e receber mais op\xe7\xf5es de im\xf3veis!')])),
                ('notificar_pendente_em', models.DateTimeField(null=True, verbose_name='Notificar pend\xeancia em', blank=True)),
                ('bairros', models.ManyToManyField(to='cidades.Bairro', blank=True)),
                ('cidade', models.ForeignKey(verbose_name='Cidade', blank=True, to='cidades.Cidade', null=True)),
                ('corretor', models.ForeignKey(verbose_name='corretor', blank=True, to='imobiliaria.Corretor', null=True)),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': 'interesse',
                'verbose_name_plural': 'interesses',
                'db_table': 'core_interesse',
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Mensagem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('assunto', models.CharField(default='', max_length=128, verbose_name='assunto', blank=True)),
                ('conteudo', models.CharField(default='', max_length=1024, verbose_name='mensagem')),
                ('do_cliente', models.BooleanField(default=False)),
                ('email_aberto', models.BooleanField(default=False)),
                ('lida', models.BooleanField(default=False)),
                ('interna', models.BooleanField(default=False)),
                ('de', models.ForeignKey(related_name='enviado_de', verbose_name='Enviado de', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('interesse', models.ForeignKey(verbose_name='interesse', to='core.Interesse')),
                ('para', models.ForeignKey(related_name='enviado_para', verbose_name='Enviado para', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': 'mensagem',
                'verbose_name_plural': 'mensagens',
                'db_table': 'core_mensagem',
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OpcaoParaVisita',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('imovel_ref', models.CharField(max_length=32, verbose_name='refer\xeancia')),
                ('quer_visitar', models.BooleanField(default=False)),
                ('avaliado', models.BooleanField(default=False)),
                ('agendado', models.BooleanField(default=False)),
                ('data_visita', models.DateTimeField(null=True, blank=True)),
                ('visitado', models.BooleanField(default=False)),
                ('imovel_nao_disponivel', models.BooleanField(default=False, verbose_name='Im\xf3vel n\xe3o dispon\xedvel (j\xe1 alugado/vendido)')),
                ('gostou', models.BooleanField(default=False)),
                ('feedback', models.CharField(default='', max_length=128, verbose_name='Feedback do cliente', blank=True)),
                ('proprietario_nao_quer_negociar', models.BooleanField(default=False, verbose_name='Propriet\xe1rio n\xe3o quer negociar (ex: n\xe3o aceita permuta)')),
                ('cliente_cancelou', models.BooleanField(default=False, verbose_name='Cliente cancelou (desistiu, n\xe3o foi)')),
                ('data_criacao', models.DateField(auto_now_add=True)),
                ('data_agendamento', models.DateTimeField(null=True, blank=True)),
                ('interesse', models.ForeignKey(verbose_name='interesse', to='core.Interesse')),
            ],
            options={
                'db_table': 'core_opcaoparavisita',
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Solicitation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('business_type', models.CharField(max_length=20, verbose_name='venda ou loca\xe7\xe3o?', choices=[('sell', 'venda'), ('rent', 'loca\xe7\xe3o')])),
                ('type', models.CharField(max_length=20, verbose_name='tipo do im\xf3vel', choices=[('house', 'casa'), ('apartment', 'apartamento'), ('commercial', 'area comercial')])),
                ('house_subtype', models.CharField(blank=True, max_length=20, null=True, verbose_name='sub-tipo', choices=[('house', 'casa'), ('townhose', 'sobrado')])),
                ('apartment_elevator', models.BooleanField(default=False, verbose_name='com elevador?')),
                ('commercial_subtype', models.CharField(blank=True, max_length=20, null=True, verbose_name='sub-tipo', choices=[('commercial', 'sala comercial'), ('hangar', 'galp\xe3o')])),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='criado')),
                ('price', models.CharField(max_length=20, verbose_name='pre\xe7o')),
                ('rooms', models.PositiveSmallIntegerField(verbose_name='n\xfamero de quartos')),
                ('region', models.CharField(max_length=100, verbose_name='regi\xe3o preferencial')),
                ('name', models.CharField(max_length=100, verbose_name='seu nome')),
                ('email', models.EmailField(max_length=100, verbose_name='seu e-mail')),
                ('phone', models.CharField(max_length=30, verbose_name='seu telefone')),
            ],
            options={
                'verbose_name': 'solicita\xe7\xe3o',
                'verbose_name_plural': 'solicita\xe7\xf5es',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('crm.atendimento',),
        ),
        migrations.AddField(
            model_name='interesse',
            name='cliente',
            field=models.ForeignKey(related_name='interesses', verbose_name='cliente', to='core.Cliente'),
            preserve_default=True,
        ),
    ]
