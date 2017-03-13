# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Atendimento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=128, verbose_name='e-mail', blank=True)),
                ('email_alternativo', models.EmailField(max_length=128, verbose_name='e-mail alternativo', blank=True)),
                ('fone', models.CharField(max_length=32, verbose_name='fone principal')),
                ('fone2', models.CharField(max_length=32, verbose_name='fone 2', blank=True)),
                ('fone3', models.CharField(max_length=32, verbose_name='fone 3 (Fixo)', blank=True)),
                ('fone4', models.CharField(max_length=32, verbose_name='fone 4', blank=True)),
                ('fone_melhorhora', models.CharField(default='', max_length=32, verbose_name='Melhor hor\xe1rio para contato', blank=True)),
                ('fone2_melhorhora', models.CharField(default='', max_length=32, verbose_name='Melhor hor\xe1rio para contato', blank=True)),
                ('fone3_melhorhora', models.CharField(default='', max_length=32, verbose_name='Melhor hor\xe1rio para contato', blank=True)),
                ('whatsapp', models.CharField(default='', max_length=32, verbose_name='WhatsApp', blank=True)),
                ('melhor_forma_contato', models.CharField(default='indiferente', max_length=16, verbose_name='Melhor forma de contato', choices=[('indiferente', 'Indiferente'), ('telefone', 'Telefone'), ('SMS', 'SMS'), ('email', 'email'), ('whatsapp', 'WhatsApp')])),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('nome', models.CharField(max_length=128, verbose_name='Nome Completo')),
                ('nome_conjuge', models.CharField(default='', max_length=128, verbose_name='Nome C\xf4njuge', blank=True)),
                ('melhor_hora', models.CharField(default='', max_length=16, verbose_name='Melhor hor\xe1rio', choices=[('qualquer', 'Qualquer hora'), ('manha', 'Manh\xe3'), ('tarde', 'A tarde'), ('noite', 'A noite')])),
                ('melhor_hora_inicio', models.TimeField(null=True, blank=True)),
                ('melhor_hora_fim', models.TimeField(null=True, blank=True)),
                ('ja_definiu_dias_para_visita', models.BooleanField(default=False, verbose_name='Melhores dias para visita')),
                ('pode_fazer_visita_na_seg', models.BooleanField(default=True, verbose_name='Segunda')),
                ('pode_fazer_visita_na_ter', models.BooleanField(default=True, verbose_name='Ter\xe7a')),
                ('pode_fazer_visita_na_qua', models.BooleanField(default=True, verbose_name='Quarta')),
                ('pode_fazer_visita_na_qui', models.BooleanField(default=True, verbose_name='Quinta')),
                ('pode_fazer_visita_na_sex', models.BooleanField(default=True, verbose_name='Sexta')),
                ('pode_fazer_visita_no_sab', models.BooleanField(default=True, verbose_name='S\xe1bado')),
                ('melhor_hora_para_visita', models.CharField(default='', max_length=128, verbose_name='Melhores hor\xe1rios', blank=True)),
                ('observacoes', models.TextField(default='', verbose_name='Observa\xe7\xf5es', blank=True)),
            ],
            options={
                'ordering': ('nome',),
                'verbose_name': 'Atendimento',
                'verbose_name_plural': 'Atendimentos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Proprietario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=128, verbose_name='e-mail', blank=True)),
                ('email_alternativo', models.EmailField(max_length=128, verbose_name='e-mail alternativo', blank=True)),
                ('fone', models.CharField(max_length=32, verbose_name='fone principal')),
                ('fone2', models.CharField(max_length=32, verbose_name='fone 2', blank=True)),
                ('fone3', models.CharField(max_length=32, verbose_name='fone 3 (Fixo)', blank=True)),
                ('fone4', models.CharField(max_length=32, verbose_name='fone 4', blank=True)),
                ('fone_melhorhora', models.CharField(default='', max_length=32, verbose_name='Melhor hor\xe1rio para contato', blank=True)),
                ('fone2_melhorhora', models.CharField(default='', max_length=32, verbose_name='Melhor hor\xe1rio para contato', blank=True)),
                ('fone3_melhorhora', models.CharField(default='', max_length=32, verbose_name='Melhor hor\xe1rio para contato', blank=True)),
                ('whatsapp', models.CharField(default='', max_length=32, verbose_name='WhatsApp', blank=True)),
                ('melhor_forma_contato', models.CharField(default='indiferente', max_length=16, verbose_name='Melhor forma de contato', choices=[('indiferente', 'Indiferente'), ('telefone', 'Telefone'), ('SMS', 'SMS'), ('email', 'email'), ('whatsapp', 'WhatsApp')])),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('nome', models.CharField(max_length=128, verbose_name='Nome Completo')),
                ('nome_conjuge', models.CharField(default='', max_length=128, verbose_name='Nome C\xf4njuge', blank=True)),
                ('observacoes', models.TextField(default='', verbose_name='Observa\xe7\xf5es', blank=True)),
                ('id_legado', models.CharField(default='', max_length=16, blank=True)),
                ('atendimento', models.ForeignKey(blank=True, to='crm.Atendimento', null=True)),
            ],
            options={
                'ordering': ('nome',),
                'verbose_name': 'Proprietario',
                'verbose_name_plural': 'Proprietarios',
            },
            bases=(models.Model,),
        ),
    ]
