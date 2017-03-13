# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from model_mommy import mommy
from model_mommy.recipe import Recipe, foreign_key

from ..models import ImovelVivaReal

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestGerarXmlVivaReal:
    pytestmark = pytest.mark.django_db

    def setup_method(self, test_method):

        self.apartamento = Recipe(ImovelVivaReal,
            tipo_imovel=ImovelVivaReal.TIPO_IMOVEL.apartamento,
        )
        self.casa = Recipe(ImovelVivaReal,
            tipo_imovel=ImovelVivaReal.TIPO_IMOVEL.casa,
        )

    def teardown_method(self, test_method):
        pass

    def test_tipo_transacao(self):
        # Dado um imovel para venda
        imovel = self.apartamento.make(
            eh_para_venda=True,
            valor_venda=300000,
        )

        # É esperado For Sale / For Rent ou Sale/Rent no tipo_imovel
        assert imovel.tipo_transacao == 'For Sale'

        # Quando para locacao e venda
        imovel.eh_para_locacao = True
        assert imovel.tipo_transacao == 'Sale/Rent'

        # Quando para locacao e venda
        imovel.eh_para_venda = False
        assert imovel.tipo_transacao == 'For Rent'

    def test_destaque(self):
        # Dado um imovel para venda
        imovel = self.apartamento.make(
            eh_para_venda=True,
            valor_venda=300000,
        )

        assert imovel.destaque == False

    def test_tipoimovel(self):
        # Dado um imovel para venda
        apto = self.apartamento.make(
            eh_para_venda=True,
            valor_venda=300000,
        )
        casa = self.casa.make(
            eh_para_venda=True,
            valor_venda=300000,
        )
        assert apto.tipo_imovel_vivareal == 'Residential / Apartment'
        assert casa.tipo_imovel_vivareal == 'Residential / Home'