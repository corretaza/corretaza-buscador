# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from unicodedata import normalize

from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.db import models

from image_cropping import ImageRatioField


@python_2_unicode_compatible
class Parceiro(models.Model):
    exibir = models.BooleanField(_('Exibir'), default=True)
    titulo = models.CharField(_('Titulo'), max_length=128, blank=True, default='')
    link = models.URLField(_('Link'), blank=True, default='')
    imagem = models.ImageField(
        _('imagem'), upload_to='parceiro_imagem/%Y/%m', blank=True, default='')
    imagem_cropping = ImageRatioField('imagem', '864x764', free_crop=True)

    class Meta:
        verbose_name = _("Parceiro")
        verbose_name_plural = _("Parceiros")

    def __str__(self):
        return self.titulo
