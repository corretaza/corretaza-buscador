# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import View, TemplateView, ListView
from django.utils import timezone
from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models import Q

from rolepermissions.verifications import has_permission

from autoatendimento.models import OpcaoParaVisita
from imobiliaria.models import Corretor
from imobiliaria.mixins import EhCorretorMixin, EhGerenteMixin

from magicemailtemplates.sender import MagicEmail

from .forms import (ImovelForm, NovoImovelPasso1Form,
                    NovoImovelPasso1ConfirmacaoForm,
                    NovoImovelPasso2Form, NovoImovelPasso3Form,
                    ImovelFotoUploadForm, ImovelFotoForm,
                    ImovelTipoForm,
                    ImovelPublicarForm, )
from ibuscador.models import Imovel, \
                             Foto, \
                             Proprietario,\
                             DescricaoImovel,\
                             DescricaoComodo, \
                             Condominio, \
                             HistoricoDeImovel
from cidades.models import Bairro, Regiao, Cidade
from .utils import obtem_campos_alterados


class NovoImovelPasso1CreateView(EhCorretorMixin, CreateView):
    model = Imovel
    form_class = NovoImovelPasso1Form
    template_name = 'imoveis/novoimovel_passo1_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        passo1_confirmacao_url = reverse(
            "imoveis.novo.imovel.passo1.confirmacao",
            kwargs={'proprietario_pk': self.object.proprietario.id})
        return HttpResponseRedirect(passo1_confirmacao_url)


class NovoImovelPasso1ConfirmacaoCreateView(EhCorretorMixin, CreateView):
    model = Imovel
    form_class = NovoImovelPasso1ConfirmacaoForm
    template_name = 'imoveis/novoimovel_passo1confirmacao_form.html'

    def get_initial(self):
        self.proprietario = get_object_or_404(
            Proprietario, pk=self.kwargs['proprietario_pk'])
        initial = {
            'proprietario': self.proprietario,
        }
        return initial

    def get_context_data(self, **kwargs):
        context = super(NovoImovelPasso1ConfirmacaoCreateView,
                        self).get_context_data(**kwargs)
        context['proprietario'] = self.proprietario
        context['imovel_list'] = Imovel.objects.filter(
            proprietario=self.proprietario)
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        maior_valor_locacao = 14000
        eh_locacao = self.object.valor_venda < maior_valor_locacao
        if eh_locacao:
            self.object.eh_para_locacao = True
            self.object.valor_locacao = self.object.valor_venda
            self.object.valor_venda = 0
        else:
            self.object.eh_para_venda = True

        eh_tipo_comercial = self.object.eh_loja or self.object.eh_sala or self.object.eh_galpao
        self.object.eh_comercial = eh_tipo_comercial
        self.object.save()

        if not HistoricoDeImovel.objects.filter(imovel=self.object):
            HistoricoDeImovel.objects.create(
                imovel=self.object,
                usuario=self.request.user,
                conteudo="Incluiu captação",
                data=timezone.now())

        messages.success(
               self.request, 'Imóvel salvo na lista de captações pendentes.')

        passo2_url = reverse(
            "imoveis.novo.imovel.passo2",
            kwargs={'pk': self.object.id})
        return HttpResponseRedirect(passo2_url)


class NovoImovelPasso2UpdateView(EhCorretorMixin, UpdateView):
    model = Imovel
    form_class = NovoImovelPasso2Form
    template_name = 'imoveis/novoimovel_passo2_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        passo3_url = reverse("imoveis.novo.imovel.passo3",
                             kwargs={'pk': self.object.id})
        return HttpResponseRedirect(passo3_url)


    def get_form_kwargs(self, **kwargs):
        kwargs = super(NovoImovelPasso2UpdateView, self).get_form_kwargs(**kwargs)
        kwargs['cidade'] = self.object.cidade.nome
        return kwargs


class NovoImovelPasso3UpdateView(EhCorretorMixin, UpdateView):
    model = Imovel
    form_class = NovoImovelPasso3Form
    template_name = 'imoveis/novoimovel_passo3_form.html'

    def get_initial(self):
        if not self.object.condominio:
            return {}
        condominio = self.object.condominio
        initial = {
            'cep': condominio.cep,
            'logradouro': condominio.logradouro,
            'numero': condominio.numero,
            'bairro': condominio.bairro,
            'regiao': condominio.regiao,
            'cidade': condominio.cidade,
        }
        return initial

    def get_form_kwargs(self, **kwargs):
        kwargs = super(NovoImovelPasso3UpdateView, self).get_form_kwargs(**kwargs)
        kwargs['cidade'] = self.object.cidade.nome
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        imovel_url = reverse("imoveis.imovel.update",
                             kwargs={'pk': self.object.id})
        return HttpResponseRedirect(imovel_url)


class NovoImovelUpdateView(EhCorretorMixin, UpdateView):
    model = Imovel
    form_class = ImovelForm
    template_name = 'imoveis/imovel_form.html'
    context_object_name = 'imovel'

    def get_context_data(self, **kwargs):
        context = super(NovoImovelUpdateView,
                        self).get_context_data(**kwargs)
        context['descricaoimovel_list'] = DescricaoImovel.objects.all()
        context['descricaocomodo_list'] = DescricaoComodo.objects.all()
        return context

    def get_success_url(self):
        return reverse("imoveis.imovel.update",
            kwargs={'pk': self.kwargs['pk']})

    def get_form_kwargs(self, **kwargs):
        kwargs = super(NovoImovelUpdateView, self).get_form_kwargs(**kwargs)
        if self.request.POST:
            kwargs['cidade'] = Cidade.objects.get(id=self.request.POST['cidade']).nome
        else:
            kwargs['cidade'] = self.object.cidade.nome
        return kwargs

    def form_valid(self, form):
        if not has_permission(self.request.user, 'alterar_imovel'):
            messages.warning(
                   self.request, 'Sem permissão para salvar informações')
            return super(NovoImovelUpdateView, self).form_invalid(form)
        self.object = form.save(commit=False)
        imovel = get_object_or_404(
            Imovel, pk=self.object.pk)
        historico = obtem_campos_alterados(imovel, self.object)
        if historico:
            HistoricoDeImovel.objects.create(
                imovel=self.object,
                usuario=self.request.user,
                conteudo=historico,
                data=timezone.now())
        messages.success(self.request, 'Informações salvas!')
        return super(NovoImovelUpdateView, self).form_valid(form)


class ImovelTipoUpdateView(EhGerenteMixin, UpdateView):
    model = Imovel
    form_class = ImovelTipoForm
    template_name = 'imoveis/imovel_tipo_form.html'
    context_object_name = 'imovel'

    def get_success_url(self):
        return reverse("core.windows_close")

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance._atualizar_slug()
        messages.success(self.request, 'Tipo do imóvel atualizado!')
        return super(ImovelTipoUpdateView, self).form_valid(form)


class ImovelFotoMixin(object):
    model = Foto
    form_class = ImovelFotoForm
    template_name = 'imoveis/foto_form.html'
    success_url = reverse_lazy('core.windows_close')


class ImovelFotoCreateView(EhCorretorMixin, ImovelFotoMixin, CreateView):

    def form_valid(self, form):
        instance = form.save(commit=False)
        imovel_pk = self.kwargs.get('imovel_pk')
        if imovel_pk:
            imovel = get_object_or_404(Imovel, pk=imovel_pk)
            instance.imovel = imovel
        instance.save()
        messages.success(self.request, 'Foto salva!')
        return super(ImovelFotoCreateView, self).form_valid(form)


class ImovelFotoUpdateView(EhCorretorMixin, ImovelFotoMixin, UpdateView):

    def form_valid(self, form):
        messages.success(self.request, 'Foto salva!')
        return super(ImovelFotoUpdateView, self).form_valid(form)


class ImovelFotoDeleteView(EhGerenteMixin, ImovelFotoMixin, DeleteView):
    template_name = 'imoveis/foto_delete_form.html'


class ImovelFotoCreateUploadView(EhCorretorMixin, CreateView):
    model = Foto
    form_class = ImovelFotoUploadForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        imovel = get_object_or_404(
            Imovel, pk=self.kwargs['imovel_pk'])
        self.object.imovel = imovel
        self.object.save()
        imovel_url = reverse("imoveis.imovel.foto.update",
                             kwargs={'pk': imovel.pk})
        messages.success(self.request, 'Foto salva!')
        return HttpResponse(imovel_url)


class ImovelPublicarUpdateView(EhGerenteMixin, UpdateView):
    model = Imovel
    form_class = ImovelPublicarForm
    template_name = 'imoveis/imovel_publicar_ou_arquivar_form.html'

    def get_initial(self):
        return {'status': Imovel.STATUS.publicado, }

    def get_success_url(self):
        return reverse("core.windows_close")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        HistoricoDeImovel.objects.create(
            imovel=self.object,
            usuario=self.request.user,
            conteudo="Publicou Imóvel",
            data=timezone.now())

        """
        TODO:
        Passar para os corretores os clientes que possivelmente tem interesse neste imovel publicado
        Interesse.objects.possiveis_clientes(param)

        parametros = {'tipo_imovel': self.object.tipo_imovel,
                      'valor': self.object.valor_venda,
                      'tipo_interesse': 'comprar'}
        if self.object.eh_para_locacao:
            parametros['valor'] = self.object.valor_locacao
            parametros['tipo_interesse'] = 'alugar'
        """
        sender = MagicEmail("{0}".format(settings.DEFAULT_FROM_EMAIL))

        current_site = Site.objects.get_current()
        subject = "Imovel publicado: Ref: {0} ".format(self.object.imovel_ref)

        data = {'domain': current_site.domain,
                'body': subject,
                'imovel': self.object, }

        email_contato = []
        for corretor in Corretor.objects.ativos():
            email_contato.append("{0} <{1}>".format(corretor.nome, corretor.email))

        sender.using_template(
            "contato_corretor_imovel_publicado", data) \
            .with_subject(subject) \
            .send_to(email_contato)

        messages.success(
               self.request, 'Imóvel Publicado!')
        return super(ImovelPublicarUpdateView, self).form_valid(form)


class ImovelArquivarUpdateView(EhGerenteMixin, UpdateView):
    model = Imovel
    form_class = ImovelPublicarForm
    template_name = 'imoveis/imovel_publicar_ou_arquivar_form.html'

    def get_initial(self):
        return {'status': Imovel.STATUS.arquivado, }

    def get_success_url(self):
        return reverse("core.windows_close")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        HistoricoDeImovel.objects.create(
            imovel=self.object,
            usuario=self.request.user,
            conteudo="Arquivou Imóvel",
            data=timezone.now())
        messages.success(
               self.request, 'Imóvel Arquivado!')
        return super(ImovelArquivarUpdateView, self).form_valid(form)


class ImovelMostrarChaveView(EhCorretorMixin, TemplateView):
    model = Imovel
    form_class = ImovelPublicarForm
    template_name = 'imoveis/imovel_mostrarchave.html'

    def get_context_data(self, **kwargs):
        context = super(ImovelMostrarChaveView,
                        self).get_context_data(**kwargs)
        imovel = get_object_or_404(Imovel, pk=self.kwargs['pk'])
        context['imovel'] = imovel
        context['proprietario'] = imovel.proprietario
        context['historico_visitas_list'] = OpcaoParaVisita.objects.filter(
            imovel_ref=imovel.imovel_ref).order_by('-data_visita')
        return context

    def get_success_url(self):
        return reverse("core.windows_close")


class ImovelRelatorioVisitaImpressaoView(EhCorretorMixin, TemplateView):
    template_name = 'imoveis/relatoriovisita_impressao.html'

    def get_context_data(self, **kwargs):
        context = super(ImovelRelatorioVisitaImpressaoView,
                        self).get_context_data(**kwargs)
        imovel = get_object_or_404(Imovel, pk=self.kwargs['pk'])
        context['imovel'] = imovel
        context['data_visita'] = timezone.now()
        return context


class BairrosPorCidade(View):

    def post(self, request, *args, **kwargs):
        data = {'options': [[bairro.id, bairro.nome]
                            for bairro in Bairro.objects.por_cidade(request.POST['cidade'])]}
        return HttpResponse(json.dumps(data), content_type="application/json")


class RegioesPorCidade(View):

    def post(self, request, *args, **kwargs):
        data = {'options': [[regiao.id, regiao.nome]
                            for regiao in Regiao.objects.por_cidade(request.POST['cidade'])]}
        return HttpResponse(json.dumps(data), content_type="application/json")


class CondominiosPorCidade(View):

    def post(self, request, *args, **kwargs):
        data = {'options': [[condominio.id, condominio.nome]
                            for condominio in Condominio.objects.por_cidade(request.POST['cidade'])]}
        return HttpResponse(json.dumps(data), content_type="application/json")


class ListaCondominiosListView(EhCorretorMixin, ListView):

    model = Condominio
    paginate_by = '100'
    context_object_name = 'condominio_list'
    template_name = 'imoveis/condominio_list.html'

    def get_context_data(self, **kwargs):
        context = super(ListaCondominiosListView,
                        self).get_context_data(**kwargs)
        palavras = self.request.GET.get('palavras') or ''
        context['palavras'] = palavras
        context['ultimas_alteracoes'] = Condominio.objects.all().order_by(
            '-atualizado_em')[:60]
        return context

    def get_queryset(self):
        palavras = self.request.GET.get('palavras')
        if not palavras:
            return Condominio.objects.all().select_related(
                'cidade', 'bairro', 'regiao', )

        return Condominio.objects.filter(
            Q(nome__icontains=palavras) |
            Q(logradouro__icontains=palavras)).select_related(
                'cidade', 'bairro', 'regiao', )


class ListaTodosImoveisListView(EhCorretorMixin, ListView):

    model = HistoricoDeImovel
    paginate_by = '200'
    context_object_name = 'imovelhistorico_list'
    template_name = 'imoveis/imovel_todos_list.html'

    def get_context_data(self, **kwargs):
        context = super(ListaTodosImoveisListView,
                        self).get_context_data(**kwargs)
        palavras = self.request.GET.get('palavras')
        context['palavras'] = palavras
        context['para_venda_pub'] = Imovel.para_venda.publicados().count()
        context['para_venda_arq'] = Imovel.para_venda.arquivados().count()
        context['para_locacao_pub'] = Imovel.para_locacao.publicados().count()
        context['para_locacao_arq'] = Imovel.para_locacao.arquivados().count()
        context['novos'] = Imovel.para_venda.novos().count()
        return context

    def get_queryset(self):
        return HistoricoDeImovel.objects.all().order_by('-id').select_related(
            'imovel', 'usuario')


class ListaCaptacoesArquivadas(EhCorretorMixin, ListView):

    model = Imovel
    paginate_by = '760'
    context_object_name = 'captacoes_list'
    template_name = 'imoveis/relatorio_captacoes_arquivadas_list.html'

    def get_queryset(self):
        usuario_logado = self.request.user.userprofile
        qs = Imovel.objects_geral.arquivados()
        exibir_apenas_do_corretor = int( self.kwargs['pk_corretor'] )

        if exibir_apenas_do_corretor or usuario_logado.is_corretor:
            qs = qs.filter(corretores__in=[usuario_logado.corretor, ])
        qs = qs.select_related(
            'cidade', 'bairro', 'regiao', 'proprietario', 'corretores', )
        return qs.order_by('atualizado_em')
