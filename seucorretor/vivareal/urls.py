# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url

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
        VivaRealXML.as_view(),
        name="vivareal.xml"),

)
