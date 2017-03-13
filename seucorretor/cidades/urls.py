# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from .views import (ListaBairroListView,
                    BairroCreateView,
                    BairroUpdateView,
                    RegiaoCreateView,
                    RegiaoUpdateView,
                    CidadeCreateView,
                    CidadeUpdateView, )


urlpatterns = patterns('',  # noqa

    url(r'^bairro/lista/$',
        ListaBairroListView.as_view(),
        name='cidades.bairro.lista'),

    url(r'^bairro/create/$',
        BairroCreateView.as_view(),
        name='cidades.bairro.create'),

    url(r'^bairro/update/(?P<pk>\d+)/$',
        BairroUpdateView.as_view(),
        name='cidades.bairro.update'),

    url(r'^regiao/create/$',
        RegiaoCreateView.as_view(),
        name='cidades.regiao.create'),

    url(r'^regiao/update/(?P<pk>\d+)/$',
        RegiaoUpdateView.as_view(),
        name='cidades.regiao.update'),

    url(r'^cidade/create/$',
        CidadeCreateView.as_view(),
        name='cidades.cidade.create'),

    url(r'^cidade/update/(?P<pk>\d+)/$',
        CidadeUpdateView.as_view(),
        name='cidades.cidade.update'),

)
