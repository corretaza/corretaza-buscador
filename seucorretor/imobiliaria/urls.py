# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url


from .views import (
    ListaDeCorretoresListView,
    ListaDeColaboradoresSiteListView, )


urlpatterns = patterns('',  # noqa

    url(r'^corretores/lista',
        ListaDeCorretoresListView.as_view(),
        name='imobiliaria.corretores.list'),

    url(r'^colaboradores/lista',
        ListaDeColaboradoresSiteListView.as_view(),
        name='imobiliaria.colaboradores.list.site'),

)
