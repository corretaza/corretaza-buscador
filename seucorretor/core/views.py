# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import RedirectView
from django.core.urlresolvers import reverse


class UserPageRedirectView(RedirectView):

    def get(self, request, *args, **kwargs):
        self.url = reverse('url_login_auth')
        profile = self.request.user.userprofile
        if profile.has_corretor:
            self.url = profile.corretor.get_absolute_url()

        elif profile.is_admin:
            self.url = reverse('core.paineldocorretor.admin')

        return super(UserPageRedirectView, self).get(request, *args, **kwargs)
