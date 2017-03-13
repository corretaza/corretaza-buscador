# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.contrib import admin

from .models import (HitCount, PageViewCount, HitDataCount, )


admin.site.register(HitCount)
admin.site.register(PageViewCount)
admin.site.register(HitDataCount)
