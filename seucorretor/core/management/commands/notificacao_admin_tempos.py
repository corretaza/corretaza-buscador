# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

import arrow
from optparse import make_option

from django.core.management.base import BaseCommand
from django.db import models
from django.db.models import F
from django.conf import settings

from magicemailtemplates.sender import MagicEmail
from imobiliaria import preferences

InteresseEstatistica = models.get_model('relatorios', 'InteresseEstatistica')
Site = models.get_model('sites', 'Site')


class Command(BaseCommand):
    help = "Create the nginx file"
    option_list = BaseCommand.option_list + (
        make_option('--mes', action='store', dest='mes', type="int", help='Especifica quando meses atras, ex: -1 = mes passado'),
    )

    def handle(self, *args, **options):
        """ """
        periodo = arrow.now()

        mes = options['mes']
        if mes:
            periodo = periodo.replace(months=mes)

        inicio, fim = periodo.span('month')

        atendimento_list = InteresseEstatistica.objects.no_periodo(
            inicio.datetime, fim.datetime).order_by('tipo_interesse', 'status')

        # TODO:
        # Tentar usar: .extra(select={'t1': 'data_contato - data_envio_contato'})

        current_site = Site.objects.get_current()
        sender = MagicEmail("{0}".format(settings.DEFAULT_FROM_EMAIL))

        subject = "Relatório mensal: Tempos nos atendimentos"

        data = {'domain': current_site.domain,
                'inicio': inicio.datetime,
                'fim': fim.datetime,
                'atendimento_list': atendimento_list,
                'mensagem': subject,
                'body': subject,
                }

        email_estats = preferences.ImobiliariaPreferences.email_notificacao_estatisticas or \
                       preferences.ImobiliariaPreferences.email_contato

        sender.using_template("notificacao_admin_tempos_semanal", data) \
              .with_subject(subject) \
              .send_to(email_estats.split(','))

        self.stdout.write('done\n')
