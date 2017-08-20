# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import (NovoProprietarioCreateView,
                    ProprietarioUpdateView,
                    ListaProprietariosListView,
                    BuscarAtendimentoPorPalavraListView, )


urlpatterns = patterns('',  # noqa

    url(r'^proprietario/create/$',
        NovoProprietarioCreateView.as_view(),
        name='crm.proprietario.create'),

    url(r'^proprietario/update/(?P<pk>\d+)/$',
        ProprietarioUpdateView.as_view(),
        name='crm.proprietario.update'),

    url(r'^proprietario/lista/$',
        ListaProprietariosListView.as_view(),
        name='crm.proprietario.lista'),

    #Others
    url(r'^lista/porpalavras/$',
        BuscarAtendimentoPorPalavraListView.as_view(),
        name='crm.lista.atendimento_por_palavra'),

)
