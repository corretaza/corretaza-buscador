# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from imobiliaria.models import Corretor


class FiltroPorDataMixin(object):

    '''
        Permite apenas para o corretor dono do painel
    '''

    def get_context_data(self, **kwargs):
        context = super(FiltroPorDataMixin, self) \
                      .get_context_data(**kwargs)

        context['anos'] = (('2015', '2015'), )
        context['meses'] = (('1', 'Jan'),
                            ('2', 'Fev'),
                            ('3', 'Mar'),
                            ('4', 'Abr'),
                            ('5', 'Mai'),
                            ('6', 'Jun'),
                            ('7', 'Jul'), )

        context['ano_value'] = self.request.GET.get('ano') or 2015
        context['mes_value'] = self.request.GET.get('mes') or 1
        return context


class FiltroPorCorretorMixin(object):

    '''
        Permite apenas para o corretor dono do painel
    '''

    def get_context_data(self, **kwargs):
        context = super(FiltroPorCorretorMixin, self) \
                      .get_context_data(**kwargs)
        context['corretor_list'] = Corretor.objects.all().order_by('nome')
        context['corretor_value'] = int(self.request.GET.get('corretor') or 0)
        return context
