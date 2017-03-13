# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import ListView

from .mixins import EhGerenteMixin

from .models import Corretor
from .models import Colaborador


class ListaDeCorretoresListView(EhGerenteMixin, ListView):

    model = Corretor
    paginate_by = '100'
    context_object_name = 'object_list'
    template_name = "imobiliaria/corretor_list.html"

    def get_queryset(self):
        return Corretor.objects.all()


class ListaDeColaboradoresSiteListView(ListView):

    model = Colaborador
    paginate_by = '100'
    context_object_name = 'object_list'
    template_name = "imobiliaria/colaborador_site_list.html"

    def get_queryset(self):
        return Colaborador.objects.ativos()
