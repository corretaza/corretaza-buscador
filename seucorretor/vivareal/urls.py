# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.views.decorators.cache import cache_page

from .views import (VivaRealFileUploadFormView,
                    VivaRealUploadCompletoListView,
                    VivaRealXML)


urlpatterns = patterns('',  # noqa

    url(r'^upload/completo',
       VivaRealUploadCompletoListView.as_view(),
       name='vivareal.upload.completo'),

    url(r'^upload/',
        VivaRealFileUploadFormView.as_view(),
        name='vivareal.upload'),

    url(r'^xml/$',
        cache_page(60 * 60 * 6)(VivaRealXML.as_view()),
        name="vivareal.xml"),

)
