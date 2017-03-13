# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

import arrow
from django.db.models import F
from .models import HitCount


class PageViewsMiddleware:

    """
    Este codigo originalmente vem do https://github.com/renyi/django-pageviews/
    Infelizmente eles nao tratam usuarios logados
    TODO: Fazer um PR lá
    """
    def process_request(self, request, *args, **kwargs):
        if request.path.startswith('/admin/') or request.path.startswith('/media/'):
            return None

        user_logged = None
        if request.user.is_authenticated():
            user_logged = request.user
        now = arrow.now()
        hit, hit_created = HitCount.objects.get_or_create(
            url=request.path, user=user_logged, year=now.year, month=now.month)
        hit.hits = F('hits') + 1
        hit.save()
        return None
