# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.http import HttpResponse
from django.conf import settings

from autoatendimento.models import Mensagem


def tracking_email_opened(request):

    if 'id' in request.GET:
        mensagem_id = request.GET.get('id')
        mensagem = Mensagem.objects.get(id=mensagem_id)
        if mensagem:
            mensagem.email_aberto = True
            mensagem.save()

    image_logo = os.path.join(settings.STATIC_ROOT,
                              'themes/sydney/img/logo_sjc_sem_nome.png')
    image_data = open(image_logo, 'rb').read()
    return HttpResponse(image_data, content_type="image/png")
