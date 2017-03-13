# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import (AtividadeCreateView,
                    AtividadeClienteCreateView,)


urlpatterns = patterns('',  # noqa

    url(r'^create/corretor/(?P<interesse_pk>\d+)/(?P<acao_id>[0-9]+)$',
        AtividadeCreateView.as_view(),
        name='atividades.corretor.create'),

    url(r'^create/cliente/(?P<interesse_pk>\d+)/(?P<acao_id>[0-9]+)$',
        AtividadeClienteCreateView.as_view(),
        name='atividades.cliente.create'),

)
