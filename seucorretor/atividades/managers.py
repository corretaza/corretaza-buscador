# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.db import models


class AtividadeQueryset(models.query.QuerySet):

    def por_corretor(self, corretor):
        qs = self.filter(interesse__corretor=corretor)
        return qs

    def no_periodo(self, inicio, fim):
        return self.filter(data__range=[inicio, fim])

    def acao_melhor_horario(self):
        return self.filter(acao__startswith='--> #11')

    def acao_agendar_visita(self):
        return self.filter(acao__startswith='--> #10')

    def acao_clicou_gostou(self):
        return self.filter(acao__startswith='--> #9',
                           objeto__exact='Gostou')

    def acao_clicou_naogostou(self):
        return self.filter(acao__startswith='--> #9',
                           objeto__exact='NÃO gostou')


class AtividadeManager(models.Manager):

    def get_queryset(self):
        return AtividadeQueryset(self.model, using=self._db)

    def por_corretor(self, corretor):
        return self.get_queryset().por_corretor(corretor)

    def no_periodo(self, inicio, fim):
        return self.get_queryset().no_periodo(inicio, fim)

    def acao_melhor_horario(self):
        return self.get_queryset().acao_melhor_horario()

    def acao_agendar_visita(self):
        return self.get_queryset().acao_agendar_visita()

    def acao_clicou_gostou(self):
        return self.get_queryset().acao_clicou_gostou()

    def acao_clicou_naogostou(self):
        return self.get_queryset().acao_clicou_naogostou()
