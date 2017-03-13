# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from .models import PageViewCount


class PageViewCountMixin(object):
    """
    Mixin para registrar que a url teve 1 acesso em um determinado instante
    Nota:
    Os acessos internos (usuario logado sao ignorados)
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            hit = PageViewCount.objects.create(url=request.path)
        return super(PageViewCountMixin, self).dispatch(
            request, *args, **kwargs)
