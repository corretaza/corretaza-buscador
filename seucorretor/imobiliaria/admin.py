# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.contrib import admin

from .models import (ImobiliariaPreferences,
                     Colaborador, )


admin.site.register(ImobiliariaPreferences)
admin.site.register(Colaborador)
