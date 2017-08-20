# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import Q

from imobiliaria.mixins import EhCorretorMixin

from .forms import (ProprietarioForm, )
from .models import Atendimento, Proprietario


class ProprietarioMixin(object):
    model = Proprietario
    form_class = ProprietarioForm


class NovoProprietarioCreateView(EhCorretorMixin, ProprietarioMixin, CreateView):

    def get_success_url(self):
        return reverse("core.windows_close")


class ProprietarioUpdateView(EhCorretorMixin, ProprietarioMixin, UpdateView):
    template_name = 'crm/proprietariocontato_form.html'

    def get_success_url(self):
        return reverse("core.windows_close")


class ListaProprietariosListView(EhCorretorMixin, ListView):

    model = Proprietario
    paginate_by = '100'
    context_object_name = 'proprietario_list'
    #template_name = 'imoveis/condominio_list.html'

    def get_context_data(self, **kwargs):
        context = super(ListaProprietariosListView,
                        self).get_context_data(**kwargs)
        palavras = self.request.GET.get('palavras')
        context['palavras'] = palavras
        return context

    def get_queryset(self):
        palavras = self.request.GET.get('palavras')
        if not palavras:
            return Proprietario.objects.all()
        # TODO: Passar estas pesquisas para um MANAGER
        return Proprietario.objects.filter(
            Q(fone__contains=palavras) |
            Q(fone2__contains=palavras) |
            Q(fone3__contains=palavras) |
            Q(fone4__contains=palavras) |
            Q(whatsapp__contains=palavras) |
            Q(email_alternativo__contains=palavras) |
            Q(nome__icontains=palavras) |
            Q(email__icontains=palavras))


class BuscarAtendimentoPorPalavraListView(ListView):
    model = Atendimento
    paginate_by = '200'
    context_object_name = 'atendimento_list'
    template_name = "crm/listaatendimento_por_palavra.html"

    def get_context_data(self, **kwargs):
        context = super(BuscarAtendimentoPorPalavraListView, self).get_context_data(**kwargs)
        buscacliente = self.request.GET.get('buscacliente')
        context['buscacliente'] = buscacliente
        return context

    def get_queryset(self):
        buscacliente = self.request.GET.get('buscacliente')
        return Atendimento.objects.por_palavras(buscacliente)
