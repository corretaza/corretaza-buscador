# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.contrib import admin

from .models import Atendimento, Proprietario


admin.site.register(Atendimento)
admin.site.register(Proprietario)
