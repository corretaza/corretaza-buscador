# -*- coding: utf-8 -*-
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.sites.models import Site
from magicemailtemplates.sender import MagicEmail
from .models import Foto, Imovel

import helper_signals


@receiver(post_save, sender=Foto)
def organizar_fotos(sender, instance, **kwargs):
    fotos_imovel = Foto.objects.filter(imovel=instance.imovel)
    helper_signals.trocar_ordem_fotos_mesma_ordem(instance, fotos_imovel)
    helper_signals.mudar_foto_principal(instance, fotos_imovel)

"""
@receiver(post_save, sender=Imovel)
def enviar_email_mudanca_status_publicado(sender, instance, **kwargs):
    if instance.status == instance.STATUS.publicado:
        sender = MagicEmail("{0}".format(settings.DEFAULT_FROM_EMAIL))
        current_site = Site.objects.get_current()
        subject = "[SJC Vale Imóveis] Novo Imóvel Publicado: Ref: {0}".format(instance.imovel_ref)
        data = {'domain': current_site.domain,
                'body': subject,
                'url': reverse('buscador.lista.imovel_referencia',
                               args=[instance.imovel_ref, ]),}
        email_contato = [corretor.email for corretor in Corretor.objects.ativos()]
        # sender.using_template(
        #     "contato_corretor_imovel_publicado", data) \
        #     .with_subject(subject) \
        #     .reply_to(settings.DEFAULT_FROM_EMAIL) \
        #     .send_to([email_contato, ])
"""