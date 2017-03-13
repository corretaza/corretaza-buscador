# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import


def userprofile_processor(request):
    profile = None
    if request.user.is_authenticated():
        try:
            profile = request.user.userprofile
        except:
            pass
    return {'userprofile': profile, }
