# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import TemplateView, ListView, RedirectView, View
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.shortcuts import get_object_or_404, redirect, render
from django.core.urlresolvers import reverse
from django.utils import timezone

from imobiliaria.mixins import EhCorretorMixin
from autoatendimento.atendimento import Atendimento, Contatos
from imobiliaria import preferences

from .forms import (BuscaInicialForm,
                    FiltroPorValorForm,
                    NovoCondominioForm,
                    HistoricoDeImovelForm,
                    ContatarAnuncianteForm, )
from .models import Imovel, Condominio, HistoricoDeImovel
from .utils import monta_queryset_com_filtros_da_pesquisa, \
                   validar_query_status_imovel, \
                   ordernar_query

from parceiros.models import Parceiro


class BuscadorHomeView(TemplateView):
    template_name = "ibuscador/home.html"

    def get_context_data(self, **kwargs):
        context = super(BuscadorHomeView, self).get_context_data(**kwargs)
        context['busca_inicial_form'] = BuscaInicialForm
        context['parceiros_list'] = Parceiro.objects.all()
        return context


class ListaDeImoveisRedirectView(RedirectView):

    def dispatch(self, request, *args, **kwargs):
        imovel_ref = self.request.GET.get('imovel_ref')
        if imovel_ref:
            try:
                return redirect(reverse('buscador.lista.imovel_referencia',
                                        args=[imovel_ref]))
            except:
                return redirect(reverse('buscador.lista.imovel_referencia',
                                        args=[0]))
        tipo_interesse = self.request.GET.get('tipo_interesse')
        tipo_imovel = self.request.GET.get('tipo_imovel')
        cidade = self.request.GET.get('cidade')
        categoria = self.request.GET.get('residencial_comercial')
        self.url = reverse(
            'ibuscador.lista.imoveispara.{0}'.format(tipo_interesse),
            args=[tipo_imovel, cidade, categoria])
        return redirect(self.url)


class ListaImoveisMixin(object):
    model = Imovel
    paginate_by = 50
    context_object_name = 'imoveis_list'
    listadeimoveis_base_template = 'ibuscador/listadeimoveis.html'

    def dispatch(self, *args, **kws):
        page = self.request.GET.get('page')
        if page:
            self.listadeimoveis_base_template =\
                'ibuscador/listadeimoveis_ajax.html'
        return super(ListaImoveisMixin, self).dispatch(*args, **kws)

    def _make_form(self, tipo_imovel, tipo_interesse ,cidade):
        init = dict(initial=self.request.GET)
        if self.request.GET:
            init = dict(data=self.request.GET)
        return FiltroPorValorForm(tipo_imovel=tipo_imovel,
                                              tipo_interesse=tipo_interesse,
                                              cidade=cidade,
                                              **init)


class ListaImoveisReferencia(View):
    def get(self, request, *args, **kwargs):
        imovel_ref = self.kwargs.get('imovel_ref')
        imovel_ref_list = Imovel.objects_geral.por_imovel_referencia(imovel_ref)
        para_avaliar = self.request.GET.get('para_avaliar', '')
        if imovel_ref_list:
            target_url = imovel_ref_list[0].get_absolute_url()
            if para_avaliar:
                target_url += '&para_avaliar={}'.format(para_avaliar)
            return redirect(target_url)
        return render(request, "ibuscador/listadeimoveis.html")


class ListaImoveisParaComprarListView(ListaImoveisMixin, ListView):

    def get_context_data(self, **kwargs):
        context = super(ListaImoveisMixin, self).get_context_data(**kwargs)
        tipo_interesse = 'comprar'
        tipo_imovel = self.kwargs.get('tipo_imovel',
                                      Imovel.TIPO_IMOVEL.apartamento)
        cidade = self.kwargs.get("cidade", "")
        context['cidade'] = cidade
        context['tipo_imovel'] = tipo_imovel
        context['tipo_interesse'] = tipo_interesse
        self.template_name = "ibuscador/listadeimoveis_{0}_{1}.html".format(
            tipo_interesse, tipo_imovel)
        context['form_filtro_valor'] = self._make_form(tipo_imovel,
                                                       tipo_interesse,
                                                       cidade)
        return context

    def get_queryset(self, **kwargs):
        imoveis_ordenados_por = self.request.GET.get('ordenar_por', 'menor_valor')
        tipo_imovel = self.kwargs.get('tipo_imovel',
                                      Imovel.TIPO_IMOVEL.apartamento)
        if tipo_imovel in ['loja', 'sala', 'galpao', 'edificio', ]:
            self.kwargs.update({'categoria': "comercial"})
        cidade = self.kwargs.get('cidade', "")
        categoria = self.kwargs.get('categoria', "residencial")
        queryset = validar_query_status_imovel(self.request)
        if categoria == 'comercial':
            queryset = queryset.comercial()
        else:
            queryset = queryset.residencial()
        form = self._make_form(tipo_imovel, "comprar", cidade)

        if form.is_valid():
            queryset = monta_queryset_com_filtros_da_pesquisa(queryset,
                                                              self.request.GET,
                                                              tipo_imovel)
            queryset = queryset.por_cidade(cidade).por_tipo_imovel(tipo_imovel)
            queryset = queryset.select_related(
                'condominio', 'cidade', 'bairro', 'regiao', 'proprietario', 'foto_principal', )
            return ordernar_query(queryset, imoveis_ordenados_por)

        queryset = queryset.por_cidade(cidade).por_tipo_imovel(tipo_imovel)
        queryset = queryset.select_related('condominio', 'cidade', 'bairro', 'regiao', 'proprietario', 'foto_principal', )
        return ordernar_query(queryset, imoveis_ordenados_por)


class ListaImoveisParaAlugarListView(ListaImoveisMixin, ListView):

    def get_context_data(self, **kwargs):
        context = super(ListaImoveisMixin, self).get_context_data(**kwargs)
        tipo_interesse = 'alugar'
        tipo_imovel = self.kwargs.get('tipo_imovel',
                                      Imovel.TIPO_IMOVEL.apartamento)
        cidade = self.kwargs.get("cidade", "")
        context['cidade'] = cidade
        context['tipo_imovel'] = tipo_imovel
        context['tipo_interesse'] = tipo_interesse
        self.template_name = "ibuscador/listadeimoveis_{0}_{1}.html".format(
            tipo_interesse, tipo_imovel)
        context['form_filtro_valor'] = self._make_form(tipo_imovel,
                                                       tipo_interesse,
                                                       cidade)
        return context

    def get_queryset(self, **kwargs):
        tipo_imovel = self.kwargs.get('tipo_imovel',
                                      Imovel.TIPO_IMOVEL.apartamento)
        if tipo_imovel in ['loja', 'sala', 'galpao', 'edificio', ]:
            self.kwargs.update({'categoria': "comercial"})

        imoveis_ordenados_por = self.request.GET.get('ordenar_por', 'menor_valor')
        queryset = validar_query_status_imovel(self.request, Imovel.para_locacao)
        cidade = self.kwargs.get('cidade', "")
        categoria = self.kwargs.get('categoria', "residencial")
        if categoria == 'comercial':
            queryset = queryset.comercial()
        else:
            queryset = queryset.residencial()
        queryset = queryset.por_cidade(cidade).por_tipo_imovel(tipo_imovel)
        form = self._make_form(tipo_imovel, "alugar", cidade)
        if form.is_valid():
            queryset = monta_queryset_com_filtros_da_pesquisa(queryset,
                                                              self.request.GET,
                                                              tipo_imovel)
        return ordernar_query(queryset, imoveis_ordenados_por)


class DetalheDoImoveisView(TemplateView):

    template_name = "ibuscador/detalhedoimovel.html"

    def get_context_data(self, **kwargs):
        tipo_interesse = self.request.GET.get('interesse', 'comprar')
        context = super(DetalheDoImoveisView, self).get_context_data(**kwargs)
        imovel = get_object_or_404(
            Imovel, slug=self.kwargs['slug'], pk=self.kwargs['pk'])
        context['imovel'] = imovel
        context['tipo_interesse'] = tipo_interesse
        context['contatar_anunciante_form'] = ContatarAnuncianteForm()
        context['imobiliaria'] = preferences.ImobiliariaPreferences

        # flat que indica que sera mostrado em um modal
        opcao_para_avaliar = self.request.GET.get('para_avaliar', '')
        if opcao_para_avaliar:
            opcao = Atendimento.com_interesse(None).get_opcao(opcao_para_avaliar)
            context['para_avaliar'] = True if opcao else False
            context['opcao'] = opcao
            context['interesse'] = opcao.interesse
        return context


class NovoCondominioCreateView(EhCorretorMixin, CreateView):

    model = Condominio
    form_class = NovoCondominioForm

    def get_success_url(self):
        return reverse("core.windows_close")


class CondominioUpdateView(EhCorretorMixin, UpdateView):

    model = Condominio
    form_class = NovoCondominioForm

    def get_success_url(self):
        return reverse("core.windows_close")


class ImoveisNovosListView(EhCorretorMixin, ListView):

    model = Imovel
    paginate_by = '150'
    context_object_name = 'imoveis_list'

    def get_queryset(self):
        return Imovel.objects_geral.novos()


class ContatarAnunciantePasso1(FormView):
    template_name = 'ibuscador/contatar_form.html'
    form_class = ContatarAnuncianteForm

    def get_initial(self):
        email = self.request.GET.get('email')
        imovel_ref = self.kwargs['imovel_ref']
        initial = {
            'email': email,
            'imovel_ref': imovel_ref,
        }
        return initial

    def get_success_url(self):
        return reverse('ibuscador.contatar.agradecimento')

    def form_valid(self, form):
        novo_contato = Contatos.novo().contato(
            form.cleaned_data['nome'],
            form.cleaned_data['email'],
            form.cleaned_data['telefone'],
            form.cleaned_data['imovel_ref'],
            form.cleaned_data['mensagem'] )
        form.envia_email()
        return super(ContatarAnunciantePasso1, self).form_valid(form)


class ImovelHistoricoCreateView(EhCorretorMixin, CreateView):
    model = HistoricoDeImovel
    form_class = HistoricoDeImovelForm

    def get_success_url(self):
        next_page = self.request.POST.get('next_page', None)
        if next_page and next_page == 'samepage':
            interesse = get_object_or_404(Interesse, pk=self.kwargs['interesse_pk'])
            return interesse.get_absolute_url()
        return reverse("core.windows_close")

    def form_valid(self, form):
        imovel = get_object_or_404(
            Imovel, pk=self.kwargs['imovel_pk'])
        self.object = form.save(commit=False)
        self.object.imovel = imovel
        self.object.data = timezone.now()
        if self.request.user:
            self.object.usuario = self.request.user
        self.object.save()
        return super(ImovelHistoricoCreateView, self).form_valid(form)


class BuscaPorPalavraListView(ListView):
    model = Imovel
    paginate_by = '200'
    context_object_name = 'imoveis_list'
    template_name = "ibuscador/listaimoveis_por_palavra.html"

    def get_context_data(self, **kwargs):
        context = super(BuscaPorPalavraListView, self).get_context_data(**kwargs)
        palavras = self.request.GET.get('palavras')
        context['palavras'] = palavras
        return context

    def get_queryset(self):
        palavras = self.request.GET.get('palavras')
        return Imovel.objects_geral.por_palavras(palavras)


