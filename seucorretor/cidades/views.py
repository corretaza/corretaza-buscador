# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q

from imobiliaria.mixins import EhGerenteMixin

from .models import Cidade, Regiao, Bairro
from .forms import BairroForm, RegiaoForm, CidadeForm


class ListaBairroListView(EhGerenteMixin, ListView):

    model = Bairro
    paginate_by = '900'
    context_object_name = 'bairro_list'

    def get_context_data(self, **kwargs):
        context = super(ListaBairroListView,
                        self).get_context_data(**kwargs)
        palavras = self.request.GET.get('palavras')
        context['palavras'] = palavras
        return context

    def get_queryset(self):
        palavras = self.request.GET.get('palavras')
        if not palavras:
            return Bairro.objects.all().order_by('cidade', 'regiao')

        return Bairro.objects.filter(
            Q(nome__icontains=palavras) |
            Q(cidade__nome__icontains=palavras)).order_by('cidade', 'regiao')


class BairroCreateView(EhGerenteMixin, CreateView):

    model = Bairro
    form_class = BairroForm

    def get_success_url(self):
        return reverse("core.windows_close")


class BairroUpdateView(EhGerenteMixin, UpdateView):

    model = Bairro
    form_class = BairroForm

    def get_success_url(self):
        return reverse("core.windows_close")


class RegiaoCreateView(EhGerenteMixin, CreateView):

    model = Regiao
    form_class = RegiaoForm

    def get_success_url(self):
        return reverse("core.windows_close")


class RegiaoUpdateView(EhGerenteMixin, UpdateView):

    model = Regiao
    form_class = RegiaoForm

    def get_success_url(self):
        return reverse("core.windows_close")


class CidadeCreateView(EhGerenteMixin, CreateView):

    model = Cidade
    form_class = CidadeForm

    def get_success_url(self):
        return reverse("core.windows_close")


class CidadeUpdateView(EhGerenteMixin, UpdateView):

    model = Cidade
    form_class = CidadeForm

    def get_success_url(self):
        return reverse("core.windows_close")
