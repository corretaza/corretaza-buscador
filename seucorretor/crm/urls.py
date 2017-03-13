# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import (NovoProprietarioCreateView,
                    ProprietarioUpdateView,
                    ListaProprietariosListView, )


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

)
