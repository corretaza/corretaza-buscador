# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest
from model_mommy import mommy
from model_mommy.recipe import Recipe, foreign_key
from cidades.models import Cidade, Regiao, Bairro
from ..models import Imovel, Foto, Proprietario
from .. import helper_signals

pytestmark = pytest.mark.django_db

@pytest.mark.django_db
class TestHelperSignals:
    pytestmark = pytest.mark.django_db

    def setup_method(self, test_method):

        self.cidade = Recipe(Cidade,
            nome='São José dos Campos',
        )

        self.regiao = Recipe(Regiao,
            nome='Oeste',
            cidade=foreign_key(self.cidade),
        )

        self.bairro = Recipe(Bairro,
            nome='Aquarius',
            regiao=foreign_key(self.regiao),
        )

        self.proprietario = Recipe(Proprietario,
            nome='Roger Waters',
            fone='12998001002',
        )

        self.casa = Recipe(Imovel,
            proprietario=foreign_key(self.proprietario),
            tipo_imovel=Imovel.TIPO_IMOVEL.casa,
            dormitorios=3,
            cidade=foreign_key(self.cidade),
            bairro=foreign_key(self.bairro),
        )

    def teardown_method(self, test_method):
        pass

    def test_auto_incremente_ordem_foto(self):
        # Dado
        imovel = self.casa.make()
        foto_1 = mommy.make(Foto, imovel=imovel, descricao="Foto1")
        foto_2 = mommy.make(Foto, imovel=imovel, descricao="Foto2")
        foto_3 = mommy.make(Foto, imovel=imovel, descricao="Foto3")

        # É esperado
        assert foto_1.ordem == 1
        assert foto_2.ordem == 2
        assert foto_3.ordem == 3

    def test_trocar_ordem_fotos_mesma_ordem(self):
        # Dado
        imovel = self.casa.make()
        foto_1 = mommy.make(Foto, imovel=imovel, descricao="Foto1")
        foto_2 = mommy.make(Foto, imovel=imovel, descricao="Foto2")

        # Quando
        foto_2.ordem = 1
        foto_2.save()

        # É esperado
        assert foto_2.ordem == 1
        assert Foto.objects.get(id=foto_1.id, imovel=imovel).ordem == 2

    def test_mudar_foto_principal(self):
        # Dado
        imovel = self.casa.make()
        imovel_2 = self.casa.make()
        foto_1 = mommy.make(Foto, imovel=imovel, descricao="Foto1", eh_principal=True)
        foto_2 = mommy.make(Foto, imovel=imovel, descricao="Foto2")
        foto_3 = mommy.make(Foto, imovel=imovel_2, descricao="Foto3", eh_principal=True)

        # É esperado
        assert foto_1.eh_principal and foto_3.eh_principal is True
        assert foto_2.eh_principal is False

        # Quando
        foto_2.eh_principal = True
        foto_2.save()
        foto_1 = Foto.objects.get(id=foto_1.id)

        # É esperado
        assert foto_2.eh_principal and foto_3.eh_principal is True
        assert foto_1.eh_principal is False