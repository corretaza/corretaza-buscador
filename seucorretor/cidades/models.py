# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from unicodedata import normalize

from django.utils.translation import ugettext_lazy as _
from django.db import models

from .managers import ManagerBase


class Cidade(models.Model):
    nome = models.CharField(verbose_name=_('Nome da cidade'), max_length=128)
    nome_abreviado = models.CharField(verbose_name=_('Abreviação'),
                                      max_length=64, blank=True, default='')
    class Meta:
        verbose_name = _("Cidade")
        verbose_name_plural = _("Cidades")

    def __unicode__(self):
        return self.nome


class Regiao(models.Model):
    nome = models.CharField(verbose_name=_('Nome da região'), max_length=64)
    cidade = models.ForeignKey(Cidade, verbose_name=_('Cidade'))

    objects = ManagerBase()

    class Meta:
        verbose_name = _("Região")
        verbose_name_plural = _("Regiões")

    def __unicode__(self):
        return "{0}".format(self.nome)

    def bairro_list(self):
        return [(bairro.id, bairro.nome)
                for bairro in Bairro.objects.filter(regiao=self)]


class Bairro(models.Model):
    nome = models.CharField(verbose_name=_('Bairro'), max_length=128)
    nome_popular = models.CharField(verbose_name=_('Nome popular'),
                                    max_length=128, blank=True)
    cidade = models.ForeignKey(Cidade, verbose_name=_('Cidade'),
                               null=True, blank=True,
                               on_delete=models.SET_NULL)
    regiao = models.ForeignKey(Regiao, verbose_name=_('Região'),
                               null=True, blank=True,
                               on_delete=models.SET_NULL)

    objects = ManagerBase()

    class Meta:
        verbose_name = _("Bairro")
        verbose_name_plural = _("Bairros")
        ordering = ['regiao', 'nome_popular', 'nome', ]

    def __unicode__(self):
        return '{0}'.format(self.descricao_verbose)

    @property
    def descricao(self):
        return self.nome_popular or self.nome

    @property
    def descricao_verbose(self):
        if self.nome_popular:
            return '{0} ({1})'.format(
              self.nome_popular, self.nome)
        return self.nome

    @property
    def descricao_sem_acento(self):
        """ Retorna o valor da descricao sem acentos. """
        try:
            sem_acentos = normalize('NFKD', self.descricao.encode('utf-8').decode('utf-8')).encode(
                            'ASCII', 'ignore')
        except:
            sem_acentos = self.descricao
        return sem_acentos


class ComEndereco(models.Model):
    cep = models.CharField(_('CEP'), max_length=16, blank=True)
    logradouro = models.CharField(_('Logradouro'), max_length=256, default='', blank=True)
    numero = models.CharField(_('Número'), max_length=16, blank=True)
    complemento = models.CharField(_('Complemento'),
                                   max_length=64, blank=True, default='',
                                   help_text='Nro. apto, Andar e Bloco')
    bairro = models.ForeignKey(Bairro, verbose_name=_('Bairro'),
                               null=True, blank=True,
                               on_delete=models.SET_NULL)
    regiao = models.ForeignKey(Regiao, verbose_name=_('Região'),
                               null=True, blank=True,
                               on_delete=models.SET_NULL)
    cidade = models.ForeignKey(Cidade, verbose_name=_('Cidade'),
                               null=True, blank=True,
                               on_delete=models.SET_NULL)

    class Meta:
        abstract = True
