# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.views.decorators.cache import cache_page

from .views import ZapImoveisXML, ImovelWebXML


urlpatterns = patterns('',  # noqa

    url(r'^xml/imovelweb/$',
        ImovelWebXML.as_view(),
        name="imovelweb.xml"),

    url(r'^xml/$',
        cache_page(60 * 60 * 6)(ZapImoveisXML.as_view()),
        name="zapimoveis.xml"),

)
