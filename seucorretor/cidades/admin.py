# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.contrib import admin

from .models import Cidade, Regiao, Bairro


admin.site.register(Cidade)
admin.site.register(Regiao)
admin.site.register(Bairro)
