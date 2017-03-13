# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import (tracking_email_opened, )


urlpatterns = patterns('',  # noqa

    url(r'^email/opened/$',
        tracking_email_opened,
        name='tracking.email.opened'),

)
