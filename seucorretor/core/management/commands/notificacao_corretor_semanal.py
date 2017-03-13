# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

import arrow
from optparse import make_option

from django.core.management.base import BaseCommand
from django.db import models
from django.conf import settings
from django.db.models import Count

from magicemailtemplates.sender import MagicEmail
from imobiliaria import preferences

Site = models.get_model('sites', 'Site')
Corretor = models.get_model('imobiliaria', 'Corretor')
UserProfile = models.get_model('signup', 'UserProfile')
HitDataCount = models.get_model('tracking', 'HitDataCount')


class Command(BaseCommand):
    """
    # Lista estatisticas da ultima semana
    ./manage.py notificacao_corretor_semanal

    # Lista estatisticas do último mes
    ./manage.py notificacao_corretor_semanal --mes=-1
    """
    help = "Envia notificacao para corretor"
    option_list = BaseCommand.option_list + (
        make_option('--mes', action='store', dest='mes', type="int",
            help='Especifica quando meses atras, ex: -1 = mes passado'),
        make_option('--data', action='store', dest='data',
            help='Especifica uma data. Por padrao é a data atual. Ex: --data=2016-08-01'),
    )

    def handle(self, *args, **options):

        data_para_pesquisa = arrow.now()
        if options['data']:
            data_para_pesquisa = arrow.get(options['data'])

        semana_passada = data_para_pesquisa.replace(weeks=-1)
        inicio, fim = semana_passada.span('week')
        periodo_descricao = '{0} a {1}'.format(inicio.format('DD/MMM'), fim.format('DD/MMM') )

        mes = options['mes']
        if mes:
            periodo = data_para_pesquisa.replace(months=mes)
            inicio, fim = periodo.span('month')
            periodo_descricao = '{0}'.format(inicio.format('MMM'))

        sender = MagicEmail("{0}".format(settings.DEFAULT_FROM_EMAIL))
        current_site = Site.objects.get_current()

        for corretor in Corretor.objects.todos():

            profile = UserProfile.objects.get(corretor=corretor)
            subject = "Relatório semanal: {0}".format(corretor.nome)
            data = {'domain': current_site.domain,
                    'corretor': corretor,
                    'inicio': inicio.datetime,
                    'fim': fim.datetime,
                    'mensagem': subject,
                    'body': subject,
                    }

            hitDatas = HitDataCount.objects.filter(
                year=fim.year, month =fim.month, period=periodo_descricao, user=profile.user)

            for item in hitDatas:
                data[item.data] = item.hits

            email_estats = preferences.ImobiliariaPreferences.email_notificacao_estatisticas or \
                           preferences.ImobiliariaPreferences.email_contato
            email_corretor = "{0} <{1}>".format(
                corretor.nome, corretor.email)

            email_list = email_estats.split(',')
            email_list.append(email_corretor)

            sender.using_template("notificacao_corretor_semanal", data) \
                .with_subject(subject) \
                .send_to(email_list)

        self.stdout.write('done\n')
