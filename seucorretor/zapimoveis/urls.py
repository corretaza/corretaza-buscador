# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import ZapImoveisXML, ImovelWebXML


urlpatterns = patterns('',  # noqa

    url(r'^xml/imovelweb/$',
        ImovelWebXML.as_view(),
        name="imovelweb.xml"),

    url(r'^xml/$',
        ZapImoveisXML.as_view(),
        name="zapimoveis.xml"),

)
