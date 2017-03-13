# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from .views import (BuscadorHomeView, ListaDeImoveisRedirectView,
                    ListaImoveisParaComprarListView,
                    ListaImoveisParaAlugarListView,
                    DetalheDoImoveisView,
                    NovoCondominioCreateView,
                    CondominioUpdateView,
                    ImoveisNovosListView,
                    ListaImoveisReferencia,
                    ContatarAnunciantePasso1,
                    ImovelHistoricoCreateView,
                    BuscaPorPalavraListView, )


urlpatterns = patterns('',  # noqa

    url(r'^$',
        BuscadorHomeView.as_view(),
        name='ibuscador.home'),

    url(r'^lista$',
        ListaDeImoveisRedirectView.as_view(),
        name='ibuscador.lista'),

    url(r'^lista/imovel_referencia/(?P<imovel_ref>[\w-]+)$',
        ListaImoveisReferencia.as_view(),
        name='buscador.lista.imovel_referencia'),

    url(r'^comprar/(?P<tipo_imovel>[\w-]+)/cidade/(?P<cidade>[\w|\W]+)/(?P<categoria>[\w-]+)/$',
        ListaImoveisParaComprarListView.as_view(),
        name='ibuscador.lista.imoveispara.comprar'),

    url(r'^alugar/(?P<tipo_imovel>[\w-]+)/cidade/(?P<cidade>[\w|\W]+)/(?P<categoria>[\w-]+)/$',
        ListaImoveisParaAlugarListView.as_view(),
        name='ibuscador.lista.imoveispara.alugar'),

    url(r'^detalhe/(?P<slug>[\w-]+)-(?P<pk>\d+)/$',
        DetalheDoImoveisView.as_view(),
        name='ibuscador.imovel.detalhe'),

    url(r'^condominio/create/$',
        NovoCondominioCreateView.as_view(),
        name='ibuscador.condominio.create'),

    url(r'^condominio/update/(?P<pk>\d+)/$',
        CondominioUpdateView.as_view(),
        name='ibuscador.condominio.update'),

    url(r'^lista/novos/imoveis/$',
        ImoveisNovosListView.as_view(),
        name='ibuscador.lista.novos.imoveis'),

    url(r'^contatar/anunciante/imovel/(?P<imovel_ref>\d+)/passo1/$',
        ContatarAnunciantePasso1.as_view(),
        name='ibuscador.contatar.anunciante.passo1'),

    url(r'^contatar/anunciante/agradecimento/$',
        TemplateView.as_view(template_name="ibuscador/contatar_agradecimento.html"),
        name='ibuscador.contatar.agradecimento'),

    url(r'^historico/(?P<imovel_pk>\d+)/create/$',
        ImovelHistoricoCreateView.as_view(),
        name='ibuscador.historico.create'),

    #Others
    url(r'^lista/porpalavras/$',
        BuscaPorPalavraListView.as_view(),
        name='ibuscador.lista.imovel_por_palavra'),

)
