# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class HitCount(models.Model):
    """
    Total de acessos por pagina mes/ano
    """
    created = models.DateTimeField(_('Created'), auto_now_add=True, editable=False)
    modified = models.DateTimeField(_('Modified'), auto_now=True, editable=False)
    url = models.CharField(_('URL'), max_length=2000)
    hits = models.PositiveIntegerField(_('Hits'), default=0)
    year = models.PositiveIntegerField(_('Ano'), default=0)
    month = models.PositiveIntegerField(_('Mes'), default=0)
    user = models.ForeignKey(User, null=True, blank=True)

    class Meta:
        ordering = ('-created', '-modified')
        get_latest_by = 'created'

    def __str__(self):
        return "{} -- {}  [{}] ".format(self.user, self.url, self.hits)


class PageViewCount(models.Model):
    """
    Cada acesso na url, mantendo data/hora
    """
    created = models.DateTimeField(_('Created'), auto_now_add=True, editable=False)
    url = models.CharField(_('URL'), max_length=2000)

    class Meta:
        ordering = ('-id', )
        get_latest_by = 'created'

    def __str__(self):
        return self.url


class HitDataCount(models.Model):
    """
    Totalizador de dados
    """
    year = models.PositiveIntegerField(_('Ano'), default=0)
    month = models.PositiveIntegerField(_('Mes'), default=0)
    period = models.CharField(_('Periodo'), max_length=32, default='Total')
    data = models.CharField(_('Dado'), max_length=512)
    hits = models.PositiveIntegerField(_('Hits'), default=0)
    user = models.ForeignKey(User, null=True, blank=True)
    modified = models.DateTimeField(_('Modified'), auto_now=True, editable=False)

    class Meta:
        ordering = ('-id', )

    def __str__(self):
        return "{0} - {1}: {2}".format(self.period, self.data, self.hits)
