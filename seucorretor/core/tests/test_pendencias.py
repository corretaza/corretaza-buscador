# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.test import TestCase

from imobiliaria.models import Corretor
from ..models import Cliente, Interesse, OpcaoParaVisita, Mensagem

from ..pendencias import PendenciasEngine


class SiteSetupEngineTest(TestCase):
    """
    Status
    ------ --
     0  Novo
     1  Perfil
     2  Buscando Imóvel
     3  Aguardando Análise
     4  Visita
     5  Proposta
     6  Contrato
     7  Pausado
     9  Finalizado
    """
    def setUp(self):

        jorge, _ = Corretor.objects.get_or_create(nome='Jorge',
                                                  email='jorge@imobi.com',
                                                  creci='123',
                                                  fone='991992993')
        fernanda, _ = Cliente.objects.get_or_create(nome='Fernanda',
                                                    email='fer@domain.com',
                                                    fone='881882883',)
        alex, _ = Cliente.objects.get_or_create(nome='Alex Lifeson',
                                                    email='alex@rush.com',
                                                    fone='881882882',)

        self.atendimento1, _ = Interesse.objects.get_or_create(cliente=fernanda,
                                                          corretor=jorge,
                                                          tipo_interesse='comprar',
                                                          tipo_imovel='apartamento',
                                                          valor=470000,
                                                          numero_dormitorios=3,
                                                          imovel_ref_inicial=439,)

        self.atendimento1.status = '2' # 'Buscando Imóvel'
        self.atendimento1.save()

        msg1, _ = Mensagem.objects.get_or_create(interesse=self.atendimento1,
                                                 assunto='Agendar visita',
                                                 conteudo='Oi, quando pode visitar o imovel?')

        self.atendimento2, _ = Interesse.objects.get_or_create(cliente=alex,
                                                          corretor=jorge,
                                                          tipo_interesse='comprar',
                                                          tipo_imovel='casa',
                                                          valor=500000,
                                                          numero_dormitorios=3,
                                                          imovel_ref_inicial=1883,)

        self.atendimento2.status = '2' # 'Buscando Imóvel'
        self.atendimento2.save()

    def tearDown(self):
        pass

    def test_deve_retornar_visita_pendente(self):
        """
        Atendimentos no Status = [2,3,4]:
        - Deve existir pelo menos 1 imovel em OpcaoParaVisita
        - Todas as opções devem estar com OpcaoParaVisita.visitado = True
        Caso contrario existe a pendencia de visitar o imovel
        """

        # Dado o atendimento1 com 1 opcao para visita não visitado
        ap439, _ = OpcaoParaVisita.objects.get_or_create(interesse=self.atendimento1,
                                                         imovel_ref='439',)
        ap439.quer_visitar = True
        ap439.avaliado = True
        ap439.visitado = False
        ap439.save()

        # Quando checamos as pendencias
        pendencias = PendenciasEngine.do(self.atendimento1).checa_pendencias_buscando_imoveis()

        # É esperado 
        self.assertEqual(pendencias, u'Falta agendar visita: 439 ')

    def test_deve_retornar_atendimento_sem_pendencia(self):
        """
        """

        # Dado o atendimento1 com 1 opcao para visita não visitado
        ap439, _ = OpcaoParaVisita.objects.get_or_create(interesse=self.atendimento1,
                                                         imovel_ref='439',)
        ap439.quer_visitar = True
        ap439.avaliado = True
        ap439.visitado = True
        ap439.save()

        # Quando checamos as pendencias
        pendencias = PendenciasEngine.do(self.atendimento1).checa_pendencias_buscando_imoveis()

        # É esperado 
        self.assertEqual(pendencias, u'')

    def test_deve_retornar_imovel_pendente_quando_nao_tem_opcaoparavisita(self):
        """
        """

        # Dado o atendimento2 sem imovel para visita
        ap1883 = "Referencia nao adicionado ao atendimento"

        # Quando checamos as pendencias
        pendencias = PendenciasEngine.do(self.atendimento2).checa_pendencias_buscando_imoveis()

        # É esperado 
        self.assertEqual(pendencias, u'Procurar mais imóveis para o cliente.')

    def test_deve_retornar_imovel_pendente_quando_opcaoparavisita_igual_naoquervisitar(self):
        """
        """

        # Dado o atendimento2 com 1 imovel que o cliente nao quer visitar (nao gostou)
        ap1883, _ = OpcaoParaVisita.objects.get_or_create(interesse=self.atendimento2,
                                                         imovel_ref='1883',)
        ap1883.quer_visitar = False
        ap1883.avaliado = True
        ap1883.save()

        # Quando checamos as pendencias
        pendencias = PendenciasEngine.do(self.atendimento2).checa_pendencias_buscando_imoveis()

        # É esperado 
        self.assertEqual(pendencias, u'Procurar mais imóveis para o cliente.')

    def test_deve_retornar_nao_pendente_quando_tem_agendamento(self):
        """
        Quando existe um agendamento de visita para o imovel, nao retorna pendencia
        """

        # Dado o atendimento1 com 1 opcao para visita não visitado
        ap439, _ = OpcaoParaVisita.objects.get_or_create(interesse=self.atendimento1,
                                                         imovel_ref='439',)
        ap439.quer_visitar = True
        ap439.avaliado = True
        ap439.visitado = False
        ap439.agendado = True
        ap439.save()

        # Quando checamos as pendencias
        pendencias = PendenciasEngine.do(self.atendimento1).checa_pendencias_buscando_imoveis()

        # É esperado 
        self.assertEqual(pendencias, u'')

    def test_deve_retornar_faltando_mensagem_quando_cliente_nao_foi_notificado(self):
        """
        Corretor encontra imoveis mas esquece de avisar o cliente sobre agendar visita
        """

        # Dado o atendimento2 com 1 imovel que o cliente nao quer visitar (nao gostou)
        ap1883, _ = OpcaoParaVisita.objects.get_or_create(interesse=self.atendimento2,
                                                         imovel_ref='1883',)
        ap1883.avaliado = False
        ap1883.save()

        # Quando checamos as pendencias
        pendencias = PendenciasEngine.do(self.atendimento2).checa_pendencias_buscando_imoveis()

        # É esperado 
        self.assertEqual(pendencias, u'Esta faltando enviar mensagem para o cliente.')
