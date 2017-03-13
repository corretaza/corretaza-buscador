# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.db import models


class InteresseEstatisticaQueryset(models.query.QuerySet):

    def por_corretor(self, corretor):
        return self.filter(corretor=corretor)

    def no_periodo(self, inicio, fim):
        return self.filter(data_contato__range=[inicio, fim])


class InteresseEstatisticaManager(models.Manager):

    def get_queryset(self):
        return InteresseEstatisticaQueryset(self.model, using=self._db)

    def por_corretor(self, corretor):
        return self.get_queryset().por_corretor(corretor)

    def no_periodo(self, inicio, fim):
        return self.get_queryset().no_periodo(inicio, fim)
