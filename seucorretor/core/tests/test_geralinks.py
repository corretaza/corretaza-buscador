# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.test import TestCase

from ..utils import gera_links


class GeraLinksTest(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_deve_converter_REF_para_link(self):

        # Dado o atendimento1 com 1 opcao para visita não visitado
        mensagem = """Favor ver os imoveis [REF:1200] fim"""

        # Quando checamos as pendencias
        mensagem_links = gera_links(mensagem, "http://abc.com/buscador/lista/imovel_referencia/")

        # É esperado
        self.assertEqual(
          mensagem_links,
          '''Favor ver os imoveis <a href="http://abc.com/buscador/lista/imovel_referencia/1200">Ref. 1200</a> fim''')
