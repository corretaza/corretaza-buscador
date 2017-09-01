# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from os import path
import base64

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.template.defaultfilters import slugify

from image_cropping import ImageRatioField
from cidades.models import ComEndereco
from seucorretor.roles import update_roles

from .behaviours import Permalinkable
from .behaviours import Preferences
from .managers import ColaboradorManager, CorretorManager


class ImobiliariaPreferences(Preferences):
    """ @see behaviours.Preferences """
    nome = models.CharField(
        _('Nome'), max_length=128, default='', blank=True)
    cep = models.CharField(
        _('CEP'), max_length=16, blank=True)
    logradouro = models.CharField(
        _('Logradouro'), max_length=256, default='', blank=True)
    numero = models.CharField(
        _('Número'), max_length=16, blank=True)
    complemento = models.CharField(
        _('Complemento'), max_length=64, blank=True, default='')
    bairro = models.CharField(
        _('Bairro'), max_length=128, default='', blank=True)
    cidade = models.CharField(
        _('Cidade'), max_length=128, default='', blank=True)
    fone1 = models.CharField(
        _('fone 1'), max_length=32, blank=True)
    fone2 = models.CharField(
        _('fone 2'), max_length=32, blank=True)
    email_contato = models.EmailField(
        _('e-mail contato'), max_length=128, blank=True)
    site_url = models.CharField(
        _('Site link'), max_length=128, blank=True)
    horario_funcionamento = models.CharField(
        _('Horário funcionamento'), max_length=128,
        default='', blank=True)
    email_inbount_mensagem = models.EmailField(
        _('e-mail inbount mensagem'), max_length=128, blank=True)
    email_notificacao_estatisticas = models.CharField(
        _('Email notificacao estatisticas'), max_length=512, blank=True)
    logo = models.ImageField(_('logo'), default='',
                             upload_to='imobiliaria/%Y/%m/%d', blank=True)
    logo_cropping = ImageRatioField('logo', '340x210')


    def __unicode__(self):
        return "{nome} - {site_url}".format(nome=self.nome, site_url=self.site_url)

    class Meta:
        verbose_name = "Preferência"
        verbose_name_plural = "Preferências"


@python_2_unicode_compatible
class Colaborador(Permalinkable, ComEndereco, models.Model):
    is_ativo = models.BooleanField(_('Ativo'), default=True)
    nome = models.CharField('nome', max_length=128)
    email = models.EmailField('e-mail', max_length=128, default='')
    fone = models.CharField('fone', max_length=32, default='')
    fone2 = models.CharField('fone 2', max_length=32, blank=True)
    fone3 = models.CharField('fone 3', max_length=32, blank=True)
    fone_detalhe = models.CharField('Operadora',
                                    max_length=32, blank=True, default='')
    fone2_detalhe = models.CharField('Operadora',
                                     max_length=32, blank=True, default='')
    fone3_detalhe = models.CharField('Operadora',
                                     max_length=32, blank=True, default='')
    whatsapp = models.CharField('WhatsApp',
                                max_length=32, blank=True, default='')

    foto = models.ImageField(_('foto'), default='',
                             upload_to='corretor_foto/%Y/%m/%d', blank=True)
    foto_cropping = ImageRatioField('foto', '296x324')
    cpf = models.CharField('CPF', max_length=16, default='', blank=True)
    rg = models.CharField('RG', max_length=16, default='', blank=True)
    data_nascimento = models.DateField(blank=True, null=True)
    data_admissao = models.DateField(blank=True, null=True)
    data_rescisao = models.DateField(blank=True, null=True)
    banco_ag_cc = models.CharField(
        'Banco, Ag e CC', max_length=128, default='', blank=True)
    email_particular = models.EmailField(
        'e-mail particular', max_length=128, default='', blank=True)
    fone_particular = models.CharField(
        'fone particular', max_length=32, default='', blank=True)
    pode_alterar_imovel = models.BooleanField(default=True)
    creci = models.CharField('CRECI', max_length=16, default='')
    comprar_contador = models.BigIntegerField('comprar cont.', default=1)
    alugar_contador = models.BigIntegerField('alugar cont.', default=1)
    pausado = models.BooleanField(_('Pausado para atendimento'), default=False)

    objects = ColaboradorManager()

    class Meta:
        ordering = ['-is_ativo', 'nome', ]
        verbose_name = 'colaborador'
        verbose_name_plural = 'colaboradores'

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.nome)
        profile = self.userprofile_set.all()
        if profile:
            update_roles(profile[0].user, self.pode_alterar_imovel)
        super(Colaborador, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core.paineladm.corretor',
                       kwargs={'pk': self.id, 'slug': self.slug})

    @property
    def foto_ok(self):
        return path.exists(self.foto.path)

    @property
    def foto_text64(self):
        return base64.b64encode(self.foto.read())


@python_2_unicode_compatible
class Corretor(Colaborador):

    objects = CorretorManager()

    class Meta:
        proxy = True
        ordering = ['-is_ativo', 'nome', ]
        verbose_name = 'corretor'
        verbose_name_plural = 'corretores'

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('core.paineladm.corretor',
                       kwargs={'pk': self.id, 'slug': self.slug})

    def get_painel_atendimentos(self):
        return reverse('core.paineladm.corretor.atendimentos',
                       kwargs={'pk': self.id, 'slug': self.slug})

    @property
    def interesse_list(self):
        # .sem_atendimento_ou_em_andamento()
        return self.interesse_set.exclude(status='9').order_by('status', '-id')

    @property
    def interesse_sem_atendimento_list(self):
        # .sem_atendimento()
        return self.interesse_set.filter(status='0').order_by('-id')

    @property
    def interesse_sem_atendimento(self):
        return self.interesse_set.filter(status='0').count()

    @property
    def interesse_atendimentos_em_andamento(self):
        # .em_andamento()
        return self.interesse_set.exclude(status='0').exclude(status='7').exclude(status='9').count()

    @property
    def interesse_pausados(self):
        # .pausados()
        return self.interesse_set.filter(status='7').count()

    @property
    def interesse_comprar(self):
        # .sem_atendimento_ou_em_andamento().tipo_comprar()
        return self.interesse_set.exclude(status='9').filter(
            tipo_interesse='comprar').count()

    @property
    def interesse_alugar(self):
        # Interesse sem_atendimento_ou_em_andamento().tipo_alugar()
        # FIX: quando migrar para django mais novo q retorna custom managers
        return self.interesse_set.exclude(status='9').filter(
            tipo_interesse='alugar').count()
