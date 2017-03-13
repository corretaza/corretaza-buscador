# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone

from braces.views import LoginRequiredMixin, UserPassesTestMixin
from autoatendimento.models import Interesse

from .models import Atividade
from .forms import AtividadeForm


class AtividadeCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Atividade
    form_class = AtividadeForm

    def test_func(self, user):
        profile = user.userprofile
        return profile.is_corretor or profile.is_admin

    def get_success_url(self):
        return reverse("core.windows_close")

    def get_context_data(self, *args, **kwargs):
        context = super(AtividadeCreateView, self).get_context_data(
            *args, **kwargs)
        interesse = Interesse.objects.get(pk=self.kwargs.get('interesse_pk'))
        return context

    def form_valid(self, form):
        interesse = get_object_or_404(
            Interesse, pk=self.kwargs['interesse_pk'])
        acao_id = self.kwargs['acao_id']
        self.object = form.save(commit=False)
        self.object.interesse = interesse
        self.object.ator = self.request.user
        if acao_id == '14':
            self.object.acao = "#14 Ligou"
            self.object.objeto = "para cliente"
        elif acao_id == '15':
            self.object.acao = "#15 Enviou"
            self.object.objeto = "email"
        elif acao_id == '16':
            self.object.acao = "#16 Enviou"
            self.object.objeto = "SMS/WhatsApp"
        else:
            self.object.acao = "#17 Registrou"
            self.object.objeto = "Histórico"
        self.object.save()

        interesse.data_ultima_comunicacao = timezone.now()
        interesse.save()
        return HttpResponseRedirect(self.get_success_url())


class AtividadeClienteCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Atividade
    form_class = AtividadeForm

    def test_func(self, user):
        profile = user.userprofile
        return profile.is_corretor or profile.is_admin

    def get_success_url(self):
        return reverse("core.windows_close")

    def get_context_data(self, *args, **kwargs):
        context = super(AtividadeClienteCreateView, self).get_context_data(
            *args, **kwargs)
        interesse = Interesse.objects.get(pk=self.kwargs.get('interesse_pk'))
        return context

    def form_valid(self, form):
        interesse = get_object_or_404(
            Interesse, pk=self.kwargs['interesse_pk'])
        acao_id = self.kwargs['acao_id']
        self.object = form.save(commit=False)
        self.object.interesse = interesse
        self.object.ator = interesse.cliente.primeiro_nome
        if acao_id == '10':
            self.object.acao = "--> #10 Ligou"
            self.object.objeto = "para corretor"
        elif acao_id == '11':
            self.object.acao = "--> #11 Enviou"
            self.object.objeto = "email"
        elif acao_id == '12':
            self.object.acao = "--> #12 Enviou"
            self.object.objeto = "SMS/WhatsApp"
        else:
            self.object.acao = "--> #13 Registrou"
            self.object.objeto = "Histórico"
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())