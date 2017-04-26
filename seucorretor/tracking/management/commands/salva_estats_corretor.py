# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

import arrow
from optparse import make_option

from django.core.management.base import BaseCommand
from django.db import models
from django.db.models import Count

Corretor = models.get_model('imobiliaria', 'Corretor')
UserProfile = models.get_model('signup', 'UserProfile')

Mensagem = models.get_model('autoatendimento', 'Mensagem')
Interesse = models.get_model('autoatendimento', 'Interesse')
OpcaoParaVisita = models.get_model('autoatendimento', 'OpcaoParaVisita')
Atividade = models.get_model('atividades', 'Atividade')
Imovel = models.get_model('ibuscador', 'Imovel')
PageViewCount = models.get_model('tracking', 'PageViewCount')
HitDataCount = models.get_model('tracking', 'HitDataCount')


class Command(BaseCommand):
    """
    # Salva os dados estatisticos do periodo atual (semana passada)
    ./manage.py salva_estats_corretor

    # Salva os dados da ultima semana com base em uma data
    ./manage.py salva_estats_corretor --data=2016-08-01

    # Salva os dados do ultimo mes
    ./manage.py salva_estats_corretor --mes=-1
    """
    help = "Salva dados estatisticos do corretor"
    option_list = BaseCommand.option_list + (
        make_option('--mes', action='store', dest='mes', type="int",
            help='Especifica quando meses atras, ex: -1 = mes passado'),
        make_option('--data', action='store', dest='data',
            help='Especifica uma data. Por padrao é a data atual. Ex: --data=2016-08-01'),
    )

    def handle(self, *args, **options):

        data_para_pesquisa = arrow.now()
        if options['data']:
            data_para_pesquisa = arrow.get(options['data'])

        semana_passada = data_para_pesquisa.replace(weeks=-1)
        inicio, fim = semana_passada.span('week')
        periodo_descricao = '{0} a {1}'.format(inicio.format('DD/MMM'), fim.format('DD/MMM') )

        mes = options['mes']
        if mes:
            periodo = data_para_pesquisa.replace(months=mes)
            inicio, fim = periodo.span('month')
            periodo_descricao = '{0}'.format(inicio.format('MMM'))

        print periodo_descricao
        print inicio, fim

        mensagem_list = Mensagem.objects.no_periodo(
            inicio.datetime, fim.datetime)

        for corretor in Corretor.objects.todos():
            msg_enviadas = mensagem_list.por_corretor(
                corretor).mensagens_enviadas()
            msg_com_resposta = mensagem_list.por_corretor(
                corretor).mensagens_com_resposta()

            interesse_novos = Interesse.objects.no_periodo(
                inicio.datetime, fim.datetime).por_corretor(corretor)
            interesse_finalizados = Interesse.objects.finalizado_no_periodo(
                inicio.datetime, fim.datetime).por_corretor(corretor)
            interesse_com_proposta = Interesse.objects.com_proposta_no_periodo(
                inicio.datetime, fim.datetime).por_corretor(corretor)
            interesse_com_contrato = Interesse.objects.com_contrato_no_periodo(
                inicio.datetime, fim.datetime).por_corretor(corretor)            

            novas_ref = OpcaoParaVisita.objects.adicionadas_no_periodo(
                inicio.datetime, fim.datetime).filter(
                interesse__corretor=corretor)
            visitas_agendadas = OpcaoParaVisita.objects.visitas_agendadas_no_periodo(
                inicio.datetime, fim.datetime).filter(
                interesse__corretor=corretor)
            visitas_efetuadas = OpcaoParaVisita.objects.visitas_efetuadas_no_periodo(
                inicio.datetime, fim.datetime).filter(
                interesse__corretor=corretor)

            atividades = Atividade.objects.no_periodo(
                inicio.datetime, fim.datetime).por_corretor(corretor)

            atendimentos_sem_msg = Interesse.objects.exclude(
                status='9').annotate(
                    qtd_msgs=Count('mensagem')).filter(corretor=corretor, qtd_msgs=1)

            atendimentos_com_1ref = Interesse.objects.exclude(
                status='9').annotate(
                    qtd_ref=Count('opcaoparavisita')).filter(corretor=corretor, qtd_ref=1)

            novas_captacoes = Imovel.objects.filter(
                data_cadastro__range=[inicio.datetime, fim.datetime], corretores__in=[corretor, ])

            painelcliente_views = PageViewCount.objects.filter(
                created__range=[inicio.datetime, fim.datetime]).exclude(
                url__startswith='/cliente/')

            # qtd de clientes que acessaram o painel
            page_views = 0
            for page in painelcliente_views:
                interesse_id = int(page.url.split('-')[-1][:-1])
                interesse = Interesse.objects.get(pk=interesse_id)
                #TODO: nao registrar cancelamentos
                if interesse.corretor == corretor:
                    page_views += 1

            interesse_cancelamentos = Interesse.objects.no_periodo(
                inicio.datetime, fim.datetime).por_corretor(corretor).filter(cancelado_pelo_cliente=True)

            data_para_gravar = {
                'interesse_novos': interesse_novos.count(),
                'interesse_finalizados': interesse_finalizados.count(),
                'interesse_com_proposta': interesse_com_proposta.count(),
                'interesse_com_contrato': interesse_com_contrato.count(),
                'msg_enviadas': msg_enviadas.count(),
                'msg_com_resposta': msg_com_resposta.count(),
                'novas_ref': novas_ref.count(),
                'visitas_agendadas': visitas_agendadas.count(),
                'visitas_efetuadas': visitas_efetuadas.count(),
                'melhor_horario': atividades.acao_melhor_horario().count(),
                'clicou_gostou': atividades.acao_clicou_gostou().count(),
                'clicou_naogostou': atividades.acao_clicou_naogostou().count(),
                'atendimentos_sem_msg': atendimentos_sem_msg.count(),
                'atendimentos_com_1ref': atendimentos_com_1ref.count(),
                'novas_captacoes': novas_captacoes.count(),
                'page_views': page_views,
                'cancelamentos': interesse_cancelamentos.count(), }
            
            profile = UserProfile.objects.get(corretor=corretor)

            print corretor
            for item, valor in data_para_gravar.iteritems():

                items = HitDataCount.objects.filter(
                    year=fim.year, month=fim.month, period=periodo_descricao,
                    user=profile.user, data=item, )
                if items.count() > 1:
                    if items[0].hits > items[1].hits:
                        items[1].delete()
                    else:
                        items[0].delete()

                hit, hit_created = HitDataCount.objects.get_or_create(
                    year=fim.year, month=fim.month, period=periodo_descricao, user=profile.user,
                    data=item, )
                hit.hits = valor
                hit.save()
                print '\t', item, valor, hit_created

        self.stdout.write('done\n')
