# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from .views import UserPageRedirectView


urlpatterns = patterns('',  # noqa

    url(r'^$',
        RedirectView.as_view(url='/buscador/'),
        name='core.showhome'),

    url(r'^favicon\.ico$',
        RedirectView.as_view(url='/static/themes/default/img/favicon/favicon.ico')),

    url(r'^builds/$',
        TemplateView.as_view(template_name="core/builds.html"),
        name='core.builds'),

    url(r'^oportunidade/freelancer/$',
        TemplateView.as_view(template_name="core/oportunidade_freelancer.html"),
        name='core.oportunidades'),

    url(r'^inovacao/setor/imobiliario/$',
        TemplateView.as_view(template_name="core/inovacao_setorimobiliario.html"),
        name='core.inovacao.setorimobiliario'),

    url(r'^userpage/$',
        UserPageRedirectView.as_view(),
        name='core.userpage'),

    url(r'^paineladm/windows_close/$', TemplateView.as_view(
        template_name="core/windows_close.html"),
        name='core.windows_close'),

    #Migracao e evitar erros 404 do site antigo
    url(r'^temp/',
        RedirectView.as_view(url='/buscador/'),
        name='core.evitar404a'),
    url(r'^license.php',
        RedirectView.as_view(url='/buscador/'),
        name='core.evitar404b'),
    url(r'^js/mage/cookies.js',
        RedirectView.as_view(url='/buscador/'),
        name='core.evitar404c'),
    url(r'^sistema/_lib/file/img/',
        RedirectView.as_view(url='/static/themes/sydney/img/logo_sjc_sem_nome.png'),
        name='core.evitar404d'),
    url(r'^modules/productpageadverts/',
        RedirectView.as_view(url='/buscador/'),
        name='core.evitar404e'),

    #XML Para ZapImoveis
    url(r'^sistema/file_zap.xml',
        RedirectView.as_view(url='/zapimoveis/xml/'),
        name='core.redirect.para.xml.do.zap'),
    #XML Para ImovelWeb
    url(r'^integracao/imovelweb/iw_ofertas.xml',
        RedirectView.as_view(url='/zapimoveis/xml/imovelweb/'),
        name='core.redirect.para.xml.da.imovelweb'),

    #XML Para ImovelWeb
    url(r'^integracao/olx/imoveis.xml',
        RedirectView.as_view(url='/zapimoveis/xml/olx/'),
        name='core.redirect.para.xml.da.olx'),


)
