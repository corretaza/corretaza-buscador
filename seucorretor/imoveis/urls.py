# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from .views import (NovoImovelPasso1CreateView,
                    NovoImovelPasso2UpdateView,
                    NovoImovelPasso3UpdateView,
                    NovoImovelUpdateView,
                    ImovelTipoUpdateView,
                    ImovelFotoCreateView,
                    ImovelFotoUpdateView,
                    ImovelFotoDeleteView,
                    ImovelFotoCreateUploadView,
                    ImovelPublicarUpdateView,
                    ImovelArquivarUpdateView,
                    ImovelMostrarChaveView,
                    ImovelRelatorioVisitaImpressaoView,
                    NovoImovelPasso1ConfirmacaoCreateView,
                    BairrosPorCidade,
                    RegioesPorCidade,
                    CondominiosPorCidade,
                    ListaCondominiosListView,
                    ListaTodosImoveisListView,
                    ListaCaptacoesArquivadas, )


urlpatterns = patterns('',  # noqa

    url(r'^novo/imovel/$',
        NovoImovelPasso1CreateView.as_view(),
        name='imoveis.novo.imovel'),

    url(r'^novo/imovel/passo1/confirmacao/(?P<proprietario_pk>[0-9]+)/$',
        NovoImovelPasso1ConfirmacaoCreateView.as_view(),
        name='imoveis.novo.imovel.passo1.confirmacao'),

    url(r'^novo/imovel/passo2/update/(?P<pk>[0-9]+)/$',
        NovoImovelPasso2UpdateView.as_view(),
        name='imoveis.novo.imovel.passo2'),

    url(r'^novo/imovel/passo3/update/(?P<pk>[0-9]+)/$',
        NovoImovelPasso3UpdateView.as_view(),
        name='imoveis.novo.imovel.passo3'),

    url(r'^novo/imovel/update/(?P<pk>[0-9]+)/$',
        NovoImovelUpdateView.as_view(),
        name='imoveis.imovel.update'),

    url(r'^imovel/tipo/update/(?P<pk>[0-9]+)/$',
        ImovelTipoUpdateView.as_view(),
        name='imoveis.imovel.tipo.update'),

    url(r'^imovel/foto/create/(?P<imovel_pk>\d+)/$',
        ImovelFotoCreateView.as_view(),
        name='imoveis.imovel.foto.create'),

    url(r'^imovel/foto/update/(?P<pk>\d+)/$',
        ImovelFotoUpdateView.as_view(),
        name='imoveis.imovel.foto.update'),

    url(r'^imovel/foto/delete/(?P<pk>\d+)/$',
        ImovelFotoDeleteView.as_view(),
        name='imoveis.imovel.foto.delete'),

    url(r'^imovel/fotos/create/upload/(?P<imovel_pk>\d+)/$',
        ImovelFotoCreateUploadView.as_view(),
        name='imoveis.imovel.foto.upload'),

    url(r'^imovel/publicar/(?P<pk>\d+)/$',
        ImovelPublicarUpdateView.as_view(),
        name='imoveis.imovel.update.publicar'),

    url(r'^imovel/arquivar/(?P<pk>\d+)/$',
        ImovelArquivarUpdateView.as_view(),
        name='imoveis.imovel.update.arquivar'),

    url(r'^imovel/mostrar/chave/(?P<pk>\d+)/$',
        ImovelMostrarChaveView.as_view(),
        name='imoveis.imovel.mostrarchave.update'),

    url(r'^imovel/relatoriovisita/impressao/(?P<pk>\d+)/$',
        ImovelRelatorioVisitaImpressaoView.as_view(),
        name='imoveis.imovel.relatoriovisita.impressao'),

    url(r'^bairros/cidade/$',
        BairrosPorCidade.as_view(),
        name='imovel.bairros.cidade'),

    url(r'^regioes/cidade/$',
        RegioesPorCidade.as_view(),
        name='imovel.regioes.cidade'),

    url(r'^condominio/cidade/$',
        CondominiosPorCidade.as_view(),
        name='imovel.condominio.cidade'),

    url(r'^condominios/lista/$',
        ListaCondominiosListView.as_view(),
        name='imovel.condominio.lista'),

    url(r'^listatodos/$',
        ListaTodosImoveisListView.as_view(),
        name='imovel.lista.todos'),

    url(r'relatorios/captacoesarquivadas/(?P<pk_corretor>\d+)/$',
        ListaCaptacoesArquivadas.as_view(),
        name='imovel.relatorios.captacoesarquivadas'),

)
