# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import BuscaCep


urlpatterns = patterns('',  # noqa

    url(r'^correios/',
        BuscaCep.as_view(), name="buscacep.correios"),

)
