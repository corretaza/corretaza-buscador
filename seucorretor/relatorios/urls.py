# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import (RelatorioMensalListView,
                    RelatorioTemposListView,
                    RelatorioIndicadoresCaptacoesListView,
                    RelatorioIndicadoresListView,
                    RelatorioNovosAtendimentosListView, )


urlpatterns = patterns('',  # noqa

    url(r'^mensal/resumo/$',
        RelatorioMensalListView.as_view(),
        name='relatorios.mensal'),

    url(r'^mensal/tempos/$',
        RelatorioTemposListView.as_view(),
        name='relatorios.mensal.tempos'),

    url(r'^indicadores/captacoes/$',
        RelatorioIndicadoresCaptacoesListView.as_view(),
        name='relatorios.indicadores.captacoes'),

    url(r'^indicadores/geral/$',
        RelatorioIndicadoresListView.as_view(),
        name='relatorios.indicadores.geral'),

    url(r'^indicadores/novosatendimentos/(?P<mes>\d+)/(?P<ano>\d+)$',
        RelatorioNovosAtendimentosListView.as_view(),
        name='relatorios.indicadores.novosatendimentos'),

)
