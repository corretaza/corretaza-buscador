# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.db import models

from autoatendimento.models import Interesse

from .managers import AtividadeManager


class Atividade(models.Model):

    interesse = models.ForeignKey(Interesse, verbose_name=_('interesse'))
    ator = models.CharField(_('Ator'), max_length=64, blank=True, default='')
    acao = models.CharField(_('Ação'), max_length=64, blank=True, default='')
    objeto = models.CharField(
        _('Objeto'), max_length=64, blank=True, default='')
    detalhe = models.TextField(
        _('Detalhe'), max_length=1024, blank=True, default='')
    data = models.DateTimeField(_('Data'), auto_now_add=True, editable=False)

    objects = AtividadeManager()

    class Meta:
        verbose_name = 'atividade'
        verbose_name_plural = 'atividades'
        ordering = ['data']

    def __unicode__(self):
        return '%s %s %s' % (self.ator, self.acao, self.objeto)

    @property
    def tipo_mensagem(self):
        return self.acao.startswith("#6") or self.acao.startswith("--> #8")
