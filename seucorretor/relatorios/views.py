# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.views.generic import ListView
from django.db.models import Count, Avg
from django.utils import timezone
from django.shortcuts import get_object_or_404

import arrow
from braces.views import LoginRequiredMixin, UserPassesTestMixin

from imobiliaria.models import Corretor
from ibuscador.models import Imovel
from tracking.models import HitDataCount
from cidades.models import Bairro
from autoatendimento.models import Contato, Interesse, Mensagem, OpcaoParaVisita

from .mixins import FiltroPorDataMixin, FiltroPorCorretorMixin
from .models import InteresseEstatistica


class RelatorioMensalListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Interesse
    paginate_by = '100'
    context_object_name = 'interesse_list'
    template_name = "relatorios/mensal.html"

    def test_func(self, user):
        return user.is_authenticated() and user.userprofile.is_admin

    def get_context_data(self, **kwargs):
        context = super(RelatorioMensalListView, self) \
                      .get_context_data(**kwargs)

        agora = timezone.now()

        start_date = datetime.datetime(2015, 6, 1, tzinfo=agora.tzinfo)
        end_date = datetime.datetime(2015, 7, 1, tzinfo=agora.tzinfo)

        periodo = Interesse.objects.filter(
            data_contato__range=(start_date, end_date))
        periodo_finalizacao = Interesse.objects.filter(
            data_finalizacao__range=(start_date, end_date))
        periodo_proposta = Interesse.objects.filter(
            data_proposta__range=(start_date, end_date))
        periodo_contrato = Interesse.objects.filter(
            data_contrato__range=(start_date, end_date))

        context['atendimentos_count'] = periodo.count()


        context['atendimentos_preco_comprar_por_regiao'] = {
                                   'Região Sul': 1,
                                   'Região Central': 1,
                                   'Região Leste': 1,
                                   'Região Oeste': 1,
                                   'Região Norte': 1,
                                   'Região Sudeste': 1, }

        context['atendimentos_preco_alugar_por_regiao'] = {
                                   'Região Sul': 1,
                                   'Região Central': 1,
                                   'Região Leste': 1,
                                   'Região Oeste': 1,
                                   'Região Norte': 1,
                                   'Região Sudeste': 1, }

        finalizou_sucesso = periodo_finalizacao.filter(tipo_finalizacao='sucesso').count()

        context['atendimentos_resumo'] = {
                                   'Aberto': periodo.count(),
                                   'Foi para propostsa': periodo_proposta.count(),
                                   'Foi para contrato': periodo_contrato.count(),
                                   'Finalizado com sucesso': finalizou_sucesso, }


        sucesso = periodo_finalizacao.filter(tipo_finalizacao='sucesso').count()
        nao_retorna = periodo_finalizacao.filter(tipo_finalizacao='nao_retorna').count()
        desistiu = periodo_finalizacao.filter(tipo_finalizacao='desistiu').count()
        sem_imovel = periodo_finalizacao.filter(tipo_finalizacao='sem_imovel').count()
        negociando_outro = periodo_finalizacao.filter(tipo_finalizacao='negociando_outro').count()
        outro = periodo_finalizacao.filter(tipo_finalizacao='outro').count()

        context['atendimentos_finalizados'] = {
                                   'Com sucesso': sucesso,
                                   'Não retorna': nao_retorna,
                                   'Desistiu': desistiu,
                                   'Sem imóvel': sem_imovel,
                                   'Negociando com outro': negociando_outro,
                                   'Outro': outro, }

        atende_ligacoes = periodo.filter(
            atende_ligacoes=False).count()
        sem_imoveis_para_perfil = periodo.filter(
            sem_imoveis_para_perfil=True).count()
        atendimentos = periodo.filter(
            atende_ligacoes=True, sem_imoveis_para_perfil=False).count()

        context['atendimentos_validos_count'] = atendimentos
        context['atendimentos_sucesso'] = {
                                   'Não atende ligações': atende_ligacoes,
                                   'Sem imóveis perfil': sem_imoveis_para_perfil,
                                   'Atendimentos': atendimentos}

        periodo = OpcaoParaVisita.objects.filter(
            interesse__data_contato__range=(start_date, end_date),
            interesse__atende_ligacoes=True,
            interesse__sem_imoveis_para_perfil=False)

        imoveis = periodo.count()
        imoveis_avaliado = periodo.filter(avaliado=True).count()
        imoveis_quervisitar = periodo.filter(avaliado=True, quer_visitar=True).count()
        imoveis_agendado = periodo.filter(agendado=True).count()
        imoveis_visitado = periodo.filter(visitado=True).count()
        imoveis_nao_gostou = periodo.filter(avaliado=True, quer_visitar=False).count()

        data = [{'name': 'Total',
                 'data': [['Total', imoveis], ]},
                {'name': 'Opções imóveis',
                 'data': [['Avaliado', imoveis_avaliado],
                          ['Quer visitar', imoveis_quervisitar],
                          ['Agendado', imoveis_agendado],
                          ['Visitado', imoveis_visitado]]}]

        context['opcoes_imoveis_count'] = imoveis
        context['opcoes_imoveis_por_atendimento'] = \
            imoveis * 1.0 / atendimentos
        context['opcoes_imoveis_taxa_quer_visitar'] = \
            imoveis_quervisitar * 100.0 / imoveis
        context['opcoes_imoveis_taxa_visitado'] = \
            imoveis_visitado * 100.0 / imoveis
        context['opcoes_imoveis_indice_nao_avaliado'] = \
            (imoveis - imoveis_avaliado) * 100.0 / imoveis
        context['opcoes_imoveis_indice_nao_gostou'] = \
            imoveis_nao_gostou * 100.0 / imoveis_avaliado
        context['opcoes_imoveis'] = data

        opcoes_com_1 = periodo.values('interesse') \
            .annotate(refs=Count('imovel_ref')).filter(refs=1).count()
        context['opcoes_com_1'] = opcoes_com_1

        opcoes_com_2 = periodo.values('interesse') \
            .annotate(refs=Count('imovel_ref')).filter(refs=2).count()
        context['opcoes_com_2'] = opcoes_com_2

        opcoes_com_3 = periodo.values('interesse') \
            .annotate(refs=Count('imovel_ref')).filter(refs=3).count()
        context['opcoes_com_3'] = opcoes_com_3

        opcoes_com_mais_de_3 = periodo.values('interesse') \
            .annotate(refs=Count('imovel_ref')).filter(refs__gt=3).count()
        context['opcoes_com_mais_de_3'] = opcoes_com_mais_de_3

        periodo = Mensagem.objects.filter(
            interesse__data_contato__range=(start_date, end_date),
            interesse__atende_ligacoes=True,
            interesse__sem_imoveis_para_perfil=False)

        # Interesse.objects.annotate(counts=Count('mensagem')).filter(counts=0)

        mensagens = periodo.filter(interna=False, do_cliente=False).count()
        respondidas = periodo.filter(do_cliente=True).count()
        email_aberto = periodo.filter(email_aberto=True).count()
        lida_no_painel = periodo.filter(lida=True).count()

        lida = email_aberto
        if lida_no_painel > email_aberto:
            lida = lida_no_painel
        context['mensagens_count'] = mensagens
        context['mensagens_por_atendimento'] = \
            mensagens * 1.0 / atendimentos
        context['mensagens_indice_leitura'] = \
            lida * 100.0 / mensagens
        context['mensagens_indice_resposta'] = \
            respondidas * 100.0 / mensagens

        data = [{'name': 'Mensagens',
                 'data': [['Mensagens', mensagens], ]},
                {'name': 'Respondidas',
                 'data': [['Respondidas', respondidas], ]},
                {'name': 'Email aberto',
                 'data': [['Email aberto', email_aberto], ]},
                {'name': 'Lida no painel',
                 'data': [['Lida no painel', lida_no_painel], ]}, ]
        context['mensagens'] = data

        return context

    def get_queryset(self):
        return Interesse.objects.all()


class RelatorioTemposListView(
        LoginRequiredMixin, UserPassesTestMixin, FiltroPorDataMixin,
        FiltroPorCorretorMixin, ListView):
    model = InteresseEstatistica
    paginate_by = '100'
    context_object_name = 'interesse_list'
    template_name = "relatorios/temposmensal.html"

    def test_func(self, user):
        return user.is_authenticated() and user.userprofile.is_admin

    def get_queryset(self):
        corretor = self.request.GET.get('corretor') or 0
        # ano = self.request.GET.get('ano') or 2015
        # mes = self.request.GET.get('mes') or 1
        if not corretor:
            return []

        agora = arrow.now()
        inicio, fim = agora.span('month')

        corretor = get_object_or_404(Corretor, pk=corretor)
        return InteresseEstatistica.objects.no_periodo(
            inicio.datetime, fim.datetime).por_corretor(corretor).order_by(
                'tipo_interesse', 'status')


class RelatorioIndicadoresCaptacoesListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Imovel
    paginate_by = '100'
    context_object_name = 'interesse_list'
    template_name = "relatorios/indicadores-captacoes.html"

    def test_func(self, user):
        return user.is_authenticated() and user.userprofile.is_admin

    def get_context_data(self, **kwargs):
        context = super(RelatorioIndicadoresCaptacoesListView, self) \
                      .get_context_data(**kwargs)

        data_para_pesquisa = arrow.now()
        corretores = Corretor.objects.ativos()

        ultimos_6meses = [0, -1, -2, -3, -4, -5]
        data = []
        for corretor in corretores:

            data_periodo = []
            for mes in ultimos_6meses:
                periodo = data_para_pesquisa.replace(months=mes)
                inicio, fim = periodo.span('month')

                captacoes = Imovel.objects_geral.filter(
                    data_cadastro__range=[inicio.datetime, fim.datetime], corretores__in=[corretor,])

                data_periodo.append([inicio.format('YYYY-MM-DD'), captacoes.count()])

            data.append({'data': data_periodo, 'name': corretor.nome.split()[0]})

        context['mensagens'] = data
        return context

    def get_queryset(self):
        return []


class RelatorioIndicadoresListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = HitDataCount
    context_object_name = 'indicadores_list'
    template_name = "relatorios/indicadores-geral.html"

    def test_func(self, user):
        return user.is_authenticated() and user.userprofile.is_admin

    def get_context_data(self, **kwargs):
        context = super(RelatorioIndicadoresListView, self).get_context_data(**kwargs)
        mes = self.request.GET.get('mes') or 'Nov'
        context['ano'] = self.request.GET.get('ano') or '2016'
        context['mes'] = mes
        # TODO: Remove this crap code
        mes_int = 0
        if mes == 'Jun':
            mes_int = 6
        elif mes == 'Jul':
            mes_int = 7
        elif mes == 'Aug':
            mes_int = 8
        elif mes == 'Sep':
            mes_int = 9
        elif mes == 'Oct':
            mes_int = 10
        elif mes == 'Nov':
            mes_int = 11
        elif mes == 'Dec':
            mes_int = 12
        context['mes_int'] = mes_int
        return context

    def get_queryset(self):
        mes = self.request.GET.get('mes') or 'Nov'
        ano = self.request.GET.get('ano') or '2017'
        return HitDataCount.objects.filter(period=mes, year=ano).order_by('data', 'user')


class RelatorioNovosAtendimentosListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Interesse
    paginate_by = '100'
    context_object_name = 'interesse_list'
    template_name = "relatorios/indicadores-novosatendimentos.html"

    def test_func(self, user):
        return user.is_authenticated() and user.userprofile.is_admin

    def get_context_data(self, **kwargs):
        context = super(RelatorioNovosAtendimentosListView, self).get_context_data(**kwargs)
        mes = self.kwargs['mes']
        ano = self.kwargs['ano']
        context['mes'] = mes
        context['ano'] = ano

        if len(mes) == 1:
            mes = '0{0}'.format(mes)

        data_para_pesquisa = arrow.get('{0}-{1}-01T00:01:00'.format(ano, mes))
        inicio, fim = data_para_pesquisa.span('month')

        periodo = Interesse.objects.filter(
            data_contato__range=(inicio.datetime, fim.datetime))
        periodo_finalizacao = Interesse.objects.filter(
            data_finalizacao__range=(inicio.datetime, fim.datetime))
        periodo_proposta = Interesse.objects.filter(
            data_proposta__range=(inicio.datetime, fim.datetime))
        periodo_contrato = Interesse.objects.filter(
            data_contrato__range=(inicio.datetime, fim.datetime))

        context['atendimentos_count'] = periodo.count()

        # Indicador 1 - % de Compra/Venda
        indicador_tipo_interesse = {}
        for tipo, desc in Interesse.TIPOS_INTERESSE:
            indicador_tipo_interesse[tipo] = periodo.filter(tipo_interesse=tipo).count()

        context['atendimentos_tipo_interesse'] = indicador_tipo_interesse

        # Indicador 2 - % por tipo de imovel
        indicador_tipos = {}
        for tipo, desc in Interesse.TIPOS_IMOVEL:
            indicador_tipos[tipo] = periodo.filter(tipo_imovel=tipo).count()

        context['atendimentos_tipo_imovel'] = indicador_tipos

        # Indicador 3 - por tipo de portal
        indicador_portal = {}
        for tipo, desc in Interesse.CRIADO_VIA_LIST:
            indicador_portal[tipo] = periodo.filter(criado_via=tipo).count()

        context['atendimentos_criado_via'] = indicador_portal

        # Indicador 4 - por bairros e regioes
        indicador_bairro = {}
        indicador_regiao = {}
        bairros = periodo.exclude(
            bairros__isnull=True).values('bairros').annotate(
            total=Count('bairros')).order_by('cidade', 'bairros')
        for item in bairros:
            bairro = get_object_or_404(Bairro, pk=item['bairros'])
            descricao_bairro = '{0}, {1}'.format(bairro.cidade.nome_abreviado, bairro.nome)
            indicador_bairro[descricao_bairro] = item['total']

            descricao_regiao = '{0}, {1}'.format(bairro.cidade.nome_abreviado, bairro.regiao.nome)
            if descricao_regiao in indicador_regiao:
                indicador_regiao[descricao_regiao] += item['total']
            else:
                indicador_regiao[descricao_regiao] = item['total']

        context['atendimentos_sem_bairro'] = periodo.filter(bairros__isnull=True).count()
        context['atendimentos_por_bairros'] = indicador_bairro
        context['atendimentos_por_regioes'] = indicador_regiao

        contatos_via_site = Contato.objects.filter(
            data__range=[inicio.datetime, fim.datetime])

        context['contatos_via_site'] = contatos_via_site.count()
        context['contatos_via_site_cliente_voltou'] = contatos_via_site.filter(cliente_voltou=True).count()
        return context

    def get_queryset(self):
        return []
        #interesse_novos = Interesse.objects.no_periodo(inicio.datetime, fim.datetime)
        #return interesse_novos







