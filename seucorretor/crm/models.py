# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.db import models

from model_utils import Choices

from .utils import formata_fone
from .managers import AtendimentoManager


@python_2_unicode_compatible
class Contato(models.Model):
    FORMAS_DE_CONTATO = Choices(('indiferente', _('Indiferente')),
                                ('telefone', _('Telefone')),
                                ('SMS', _('SMS')),
                                ('email', _('email')),
                                ('whatsapp', _('WhatsApp')), )
    email = models.EmailField(_('e-mail'), max_length=128, blank=True)
    email_alternativo = models.EmailField(_('e-mail alternativo'), max_length=128, blank=True)
    fone = models.CharField(_('fone principal'), max_length=32)
    fone2 = models.CharField(_('fone 2'), max_length=32, blank=True)
    fone3 = models.CharField(_('fone 3 (Fixo)'), max_length=32, blank=True)
    fone4 = models.CharField(_('fone 4'), max_length=32, blank=True)
    fone_melhorhora = models.CharField(
        _('Melhor horário para contato'), max_length=32,
        blank=True, default='')
    fone2_melhorhora = models.CharField(
        _('Melhor horário para contato'), max_length=32,
        blank=True, default='')
    fone3_melhorhora = models.CharField(
        _('Melhor horário para contato'), max_length=32,
        blank=True, default='')
    whatsapp = models.CharField(
        _('WhatsApp'), max_length=32, blank=True, default='')
    melhor_forma_contato = models.CharField(
        _('Melhor forma de contato'), max_length=16,
        choices=FORMAS_DE_CONTATO, default=FORMAS_DE_CONTATO.indiferente)

    class Meta:
        abstract = True

    def __str__(self):
        return self.email or self.fone or ''

    @property
    def fone_verbose(self):
        return formata_fone(self.fone)

    @property
    def fone2_verbose(self):
        return formata_fone(self.fone2)

    @property
    def fone3_verbose(self):
        return formata_fone(self.fone3)

    @property
    def fone4_verbose(self):
        return formata_fone(self.fone4)


class Atendimento(Contato):
    LISTA_MELHOR_HORARIO = (
        ('qualquer', 'Qualquer hora'),
        ('manha', 'Manhã'),
        ('tarde', 'A tarde'),
        ('noite', 'A noite'),
    )
    TIPOS_URGENCIA = (
        ('0', _('Muito urgente, preciso achar um imóvel em menos de 1 semana/mes')),
        ('1', _('Urgente, preciso achar um imóvel dentro 3 meses')),
        ('2', _('Não urgente, estou pesquisando para comprar daqui 6 meses ou 1 ano')),
        ('3', _('Investidor, quero o melhor custo/benefício')),
        ('9', _('Não informado')),
    )
    data_criacao = models.DateTimeField(auto_now_add=True, editable=False)
    nome = models.CharField(_('Nome Completo'), max_length=128)
    nome_conjuge = models.CharField(_('Nome Cônjuge'), max_length=128,
                                    default='', blank=True)
    melhor_hora = models.CharField(
        'Melhor horário', max_length=16, default='',
        choices=LISTA_MELHOR_HORARIO)
    melhor_hora_inicio = models.TimeField(
        editable=True, blank=True, null=True)
    melhor_hora_fim = models.TimeField(
        editable=True, blank=True, null=True)
    ja_definiu_dias_para_visita = models.BooleanField(
        'Melhores dias para visita', default=False)
    pode_fazer_visita_na_seg = models.BooleanField(
        'Segunda', default=True)
    pode_fazer_visita_na_ter = models.BooleanField(
        'Terça', default=True)
    pode_fazer_visita_na_qua = models.BooleanField(
        'Quarta', default=True)
    pode_fazer_visita_na_qui = models.BooleanField(
        'Quinta', default=True)
    pode_fazer_visita_na_sex = models.BooleanField(
        'Sexta', default=True)
    pode_fazer_visita_no_sab = models.BooleanField(
        'Sábado', default=True)
    melhor_hora_para_visita = models.CharField(
        'Melhores horários', max_length=128, blank=True, default='')
    observacoes = models.TextField(
        _('Observações'), blank=True, default='')
    urgencia = models.CharField(
        _('Urgencia'), max_length=2,
        choices=TIPOS_URGENCIA, default='9')

    objects = AtendimentoManager()

    class Meta:
        verbose_name = _('Atendimento')
        verbose_name_plural = _('Atendimentos')
        ordering = ('nome', )

    def __str__(self):
        return self.nome

    @property
    def primeiro_nome(self):
        return self.nome.split()[0]

    @property
    def melhor_hora_para_visita_verbose(self):
        melhor_hora = ''
        if self.ja_definiu_dias_para_visita:
            melhor_hora += 'Seg ' if self.pode_fazer_visita_na_seg else ''
            melhor_hora += 'Ter ' if self.pode_fazer_visita_na_ter else ''
            melhor_hora += 'Qua ' if self.pode_fazer_visita_na_qua else ''
            melhor_hora += 'Qui ' if self.pode_fazer_visita_na_qui else ''
            melhor_hora += 'Sex ' if self.pode_fazer_visita_na_sex else ''
            melhor_hora += 'Sáb ' if self.pode_fazer_visita_no_sab else ''
            melhor_hora += self.melhor_hora_para_visita
        return melhor_hora

    @property
    def melhor_hora_contato_verbose(self):
        melhor_hora_contato = ''
        if self.melhor_hora or self.melhor_forma_contato != 'indiferente':
            melhor_hora_contato += self.melhor_hora
            melhor_hora_contato += " (ou entre {0} e {1})".format(
                self.melhor_hora_inicio, self.melhor_hora_fim) if self.melhor_hora_inicio else ''
        return melhor_hora_contato

    def atualiza_fone(self, novo_fone):
        if not self.fone2:
            self.fone2 = novo_fone
        elif not self.fone3:
            self.fone3 = novo_fone
        elif not self.fone4:
            self.fone4 = novo_fone
        self.save()
        return self

    def atualiza_email(self, novo_email):
        if not self.email:
            self.email = novo_email
        elif not self.email_alternativo:
            self.email_alternativo = novo_email
        self.save()
        return self


@python_2_unicode_compatible
class Proprietario(Contato):

    data_criacao = models.DateTimeField(auto_now_add=True, editable=False)
    nome = models.CharField(_('Nome Completo'), max_length=128)
    nome_conjuge = models.CharField(_('Nome Cônjuge'), max_length=128,
                                    default='', blank=True)
    observacoes = models.TextField(
        _('Observações'), blank=True, default='')
    atendimento = models.ForeignKey(
        Atendimento, null=True, blank=True)
    id_legado = models.CharField(
        max_length=16, blank=True, default='')

    class Meta:
        verbose_name = _('Proprietario')
        verbose_name_plural = _('Proprietarios')
        ordering = ('nome', )

    def __str__(self):
        proprietario = self.nome
        if self.nome_conjuge:
            proprietario = "{0} / {1}".format(self.nome, self.nome_conjuge)
        if self.fone or self.fone3:
            proprietario += " ({}, {})".format(self.fone, self.fone3)
        return proprietario
