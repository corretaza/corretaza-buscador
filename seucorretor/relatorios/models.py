# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.db import models

from autoatendimento.models import Interesse, Mensagem

from .managers import InteresseEstatisticaManager


def convert_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    return '{0}h {1}min'.format(hours, minutes)


class InteresseEstatistica(Interesse):

    objects = InteresseEstatisticaManager()

    class Meta:
        proxy = True

    def tempo_cadastro(self):
        delta = self.data_contato - self.data_envio_contato
        return convert_timedelta(delta)

    def primeira_mensagem_contato(self):
        mensagem_list = Mensagem.objects.filter(
            interesse=self, interna=True).order_by('data')
        if not mensagem_list:
            return None
        return mensagem_list[0].data

    def tempo_envio_para_corretor(self):
        data_primeira_mensagem = self.primeira_mensagem_contato()
        if data_primeira_mensagem:
            delta = data_primeira_mensagem - self.data_envio_contato
            return convert_timedelta(delta)
        return None

    def tempo_inicio_atendimento(self):
        mensagem_list = Mensagem.objects.filter(
            interesse=self).order_by('data')
        if not mensagem_list:
            return None
        delta = mensagem_list[0].data - self.data_envio_contato
        return convert_timedelta(delta)

    def leu_email(self):
        mensagem_list = Mensagem.objects.filter(
            interesse=self, email_aberto=True)
        if not mensagem_list:
            return False
        return True

    def respondido(self):
        mensagem_list = Mensagem.objects.filter(
            interesse=self, do_cliente=True)
        if not mensagem_list:
            return False
        return True
