# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.contrib import admin

from .models import (Imovel, FormaDePagamento, Condominio, AreaDeLazer,
                     BairroComImoveis, Foto,
                     DescricaoImovel, DescricaoComodo, HistoricoDeImovel, )


admin.site.register(FormaDePagamento)
admin.site.register(AreaDeLazer)
admin.site.register(Condominio)
admin.site.register(Imovel)
admin.site.register(BairroComImoveis)
admin.site.register(Foto)
admin.site.register(DescricaoImovel)
admin.site.register(DescricaoComodo)
admin.site.register(HistoricoDeImovel)
