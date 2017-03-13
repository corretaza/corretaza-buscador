# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from model_mommy import mommy
from model_mommy.recipe import Recipe, foreign_key

from cidades.models import Cidade, Regiao, Bairro
from ..models import Imovel, Condominio, Proprietario

pytestmark = pytest.mark.django_db

@pytest.mark.django_db
class TestFiltrarImoveis:
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

        self.condominio = Recipe(Condominio,
            cep='12120000',
            logradouro='Rua Tubarão Branco',
            numero='900',
            bairro=foreign_key(self.bairro),
            regiao=foreign_key(self.regiao),
            cidade=foreign_key(self.cidade),
        )

        self.proprietario = Recipe(Proprietario,
            nome='Roger Waters',
            fone='12998001002',
        )

        self.apartamento = Recipe(Imovel,
            proprietario=foreign_key(self.proprietario),
            tipo_imovel=Imovel.TIPO_IMOVEL.apartamento,
            dormitorios=2,
            condominio=foreign_key(self.condominio),
            cidade=foreign_key(self.cidade),
            bairro=foreign_key(self.bairro),
            complemento='Apto 14A',
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

    def test_lista_todos_imoveis(self):
        # Dado
        apto = self.apartamento.make(
            eh_para_venda=True,
            valor_venda=300000,
        )

        # Quando
        todos_imoveis = Imovel.objects.all()

        # É esperado
        assert len(todos_imoveis) == 1
        assert todos_imoveis[0] == apto

    def test_lista_imoveis_publicados(self):
        # Dado
        casa_publicada = self.casa.make(status=Imovel.STATUS.publicado)
        casa_nao_publicada = self.casa.make()

        # Quando
        resultado = Imovel.objects_geral.publicados()

        # É esperado
        assert casa_publicada in resultado
        assert casa_nao_publicada not in resultado
        assert len(resultado) == 1

    def test_lista_imoveis_novos(self):
        # Dado
        casa_nova = self.casa.make(status=Imovel.STATUS.novo)
        casa_publicada = self.casa.make(status=Imovel.STATUS.publicado)

        # Quando
        resultado = Imovel.objects_geral.novos()

        # É esperado
        assert casa_nova in resultado
        assert casa_publicada not in resultado
        assert len(resultado) == 1

    def test_lista_imoveis_arquivados(self):
        # Dado
        casa_arquivada = self.casa.make(status=Imovel.STATUS.arquivado)
        casa_nova = self.casa.make(status=Imovel.STATUS.novo)
        casa_publicada = self.casa.make(status=Imovel.STATUS.publicado)

        # Quando
        resultado = Imovel.objects_geral.arquivados()

        # É esperado
        assert casa_arquivada in resultado
        assert casa_publicada and casa_nova not in resultado
        assert len(resultado) == 1

    def test_lista_imoveis_para_venda_por_tipo_imovel(self):
        # Dado
        apto150A = self.apartamento.make(
            eh_para_venda=True,
            valor_venda=300000,
            complemento='Apto 150A')
        apto90A = self.apartamento.make(
            eh_para_venda=True,
            valor_venda=260000,
            complemento='Apto 90A')
        casa = self.casa.make(
            eh_para_venda=True,
            valor_venda=260000)
        apto_locacao = self.apartamento.make(
            eh_para_locacao=True,
            valor_venda=800)

        # Quando
        resultado = Imovel.para_venda.por_tipo_imovel(
            Imovel.TIPO_IMOVEL.apartamento)

        # É esperado
        assert apto150A, apto90A in resultado
        assert casa, apto_locacao not in resultado

    def test_lista_imoveis_para_locacao(self):
        # Dado
        apto150A = self.apartamento.make(
            eh_para_locacao=True,
            valor_locacao=300000,
            complemento='Apto 150A')
        apto90A = self.apartamento.make(
            eh_para_venda=True,
            valor_venda=260000,
            complemento='Apto 90A')

        # Quando
        resultado = Imovel.para_locacao.por_tipo_imovel(
            Imovel.TIPO_IMOVEL.apartamento)

        # É esperado
        assert apto150A in resultado
        assert apto90A not in resultado

    def test_lista_imoveis_por_faixa_de_valor_venda(self):
        # Dado
        apto150A = self.apartamento.make(
            eh_para_venda=True,
            valor_venda=300000,
            complemento='Apto 150A')
        apto90A = self.apartamento.make(
            eh_para_venda=True,
            valor_venda=260000,
            complemento='Apto 90A')
        apto14A = self.apartamento.make(
            eh_para_venda=True,
            valor_venda=240000,
            complemento='Apto 14A')

        # Quando
        resultado = Imovel.para_venda.por_valor_max(250000)

        # É esperado
        assert len(resultado) == 1
        assert apto14A in resultado

        # Quando
        resultado = Imovel.para_venda.por_valor_min(250000).por_valor_max(310000)

        # É esperado
        assert len(resultado) == 2
        assert apto150A in resultado
        assert apto90A in resultado

        # Quando
        resultado = Imovel.para_venda.por_valor_max(239000)

        # É esperado
        assert len(resultado) == 0

    def test_lista_imoveis_por_faixa_de_valor_alugar(self):
        # Dado
        apto150A = self.apartamento.make(
            eh_para_locacao=True,
            valor_locacao=2000,
            complemento='Apto 150A')
        apto90A = self.apartamento.make(
            eh_para_locacao=True,
            valor_locacao=1800,
            complemento='Apto 90A')
        apto14A = self.apartamento.make(
            eh_para_locacao=True,
            valor_locacao=1400,
            complemento='Apto 14A')

        # Quando
        resultado = Imovel.para_locacao.por_valor_max(1400)

        # É esperado
        assert len(resultado) == 1
        assert apto14A in resultado

        # Quando
        resultado = Imovel.para_locacao.por_valor_min(1500).por_valor_max(2100)

        # É esperado
        assert len(resultado) == 2
        assert apto150A in resultado
        assert apto90A in resultado

        # Quando
        resultado = Imovel.para_locacao.por_valor_max(1300)

        # É esperado
        assert len(resultado) == 0

    def test_lista_apartamento_por_min_dormitorio(self):
        # Dado
        apto150A = self.apartamento.make(
            eh_para_venda=True,
            valor_venda=300000,
            dormitorios=3,
            complemento='Apto 150A', )
        apto90A = self.apartamento.make(
            eh_para_venda=True,
            valor_venda=260000,
            dormitorios=2,
            complemento='Apto 90A', )
        apto14A = self.apartamento.make(
            eh_para_venda=True,
            valor_venda=240000,
            dormitorios=1,
            complemento='Apto 14A', )

        # Quando
        resultado = Imovel.para_venda.por_tipo_imovel(
            Imovel.TIPO_IMOVEL.apartamento).por_min_dormitorio(1)

        # É esperado
        assert len(resultado) == 3
        assert apto14A in resultado

        # Quando
        resultado = Imovel.para_venda.por_tipo_imovel(
            Imovel.TIPO_IMOVEL.apartamento).por_min_dormitorio(2)

        # É esperado
        assert len(resultado) == 2
        assert apto150A in resultado
        assert apto90A in resultado

        # Quando
        resultado = Imovel.para_venda.por_tipo_imovel(
            Imovel.TIPO_IMOVEL.apartamento).por_min_dormitorio(3)

        # É esperado
        assert len(resultado) == 1
        assert apto150A in resultado

    def test_lista_imoveis_por_qtd_min_vagas_garagem(self):
        # Dado
        apto150A = self.apartamento.make(
            eh_para_venda=True,
            valor_venda=300000, vagas_garagem=2,
            complemento='Apto 150A', )
        apto90A = self.apartamento.make(
            eh_para_venda=True,
            valor_venda=260000, vagas_garagem=2,
            complemento='Apto 90A', )
        apto14A = self.apartamento.make(
            eh_para_venda=True,
            valor_venda=240000, vagas_garagem=0,
            complemento='Apto 14A', )

        # Quando
        resultado = Imovel.para_venda.por_min_vagas_garagem(2)

        # É esperado
        assert len(resultado) == 2
        assert apto150A and apto90A in resultado

        # Quando
        resultado = Imovel.para_venda.por_tipo_imovel(
            Imovel.TIPO_IMOVEL.apartamento).por_min_vagas_garagem(1)

        # É esperado
        assert len(resultado) == 2
        assert apto14A not in resultado

    def test_lista_imoveis_por_min_area_construida(self):
        # Dado
        apto150A = self.apartamento.make(
            eh_para_venda=True, 
            valor_venda=300000, dormitorios=3, area_construida=72,
            complemento='Apto 150A', )
        apto90A = self.apartamento.make(
            eh_para_venda=True,
            valor_venda=260000, dormitorios=2, area_construida=67,
            complemento='Apto 90A', )
        apto14A = self.apartamento.make(
            eh_para_venda=True,
            valor_venda=240000, dormitorios=1, area_construida=58,
            complemento='Apto 14A', )

        # Quando
        resultado = Imovel.para_venda.por_min_area_construida(75)

        # É esperado
        assert len(resultado) == 0

        # Quando
        resultado = Imovel.para_venda.por_tipo_imovel(
            Imovel.TIPO_IMOVEL.apartamento).por_min_area_construida(60)

        # É esperado
        assert len(resultado) == 2
        assert apto90A and apto150A in resultado
        assert apto14A not in resultado

    def test_lista_casas_por_min_area_construida(self):
        # Dado
        casa150A = self.casa.make(
            eh_para_venda=True,
            valor_venda=300000, dormitorios=3, area_construida=72,
            complemento='Apto 150A', )
        casa90A = self.casa.make(
            eh_para_venda=True,
            valor_venda=260000, dormitorios=2, area_construida=67,
            complemento='Apto 90A', )
        casa14A = self.casa.make(
            eh_para_venda=True,
            valor_venda=240000, dormitorios=1, area_construida=58,
            complemento='Apto 14A', )

        # Quando
        resultado = Imovel.para_venda.por_tipo_imovel(
            Imovel.TIPO_IMOVEL.casa).por_min_area_construida(60)

        # É esperado
        assert len(resultado) == 2
        assert casa90A and casa150A in resultado
        assert casa14A not in resultado

    def test_lista_imovel_eh_casa_sobrado(self):
        # Dado
        casa150 = self.casa.make(
            eh_para_venda=True,
            eh_casa_sobrado=True)
        apto150A = self.apartamento.make(
            eh_para_venda=True)

        # Quando
        resultado_casa = Imovel.objects_geral.por_tipo_imovel(Imovel.TIPO_IMOVEL.casa).eh("casa_sobrado")
        resultado_imovel = Imovel.objects_geral.eh("casa_sobrado")

        # É esperado
        assert len(resultado_casa) and len(resultado_imovel) == 1
        assert casa150 in resultado_casa and resultado_imovel
        assert apto150A not in resultado_casa and resultado_imovel

    def test_lista_imovel_eh_casa_edicula(self):
        # Dado
        casa150 = self.casa.make(
            eh_para_venda=True,
            eh_casa_edicula=True)
        casa151 = self.casa.make(
            eh_para_venda=True,
            eh_casa_edicula=True)
        apto150A = self.apartamento.make(
            eh_para_venda=True)

        # Quando
        resultado = Imovel.objects_geral.por_tipo_imovel(Imovel.TIPO_IMOVEL.casa).eh("casa_edicula")

        # É esperado
        assert len(resultado) == 2
        assert casa150 and casa151 in resultado
        assert apto150A not in resultado

    def test_lista_imovel_eh_casa_sobreloja(self):
        # Dado
        casa150 = self.casa.make(
            eh_para_venda=True,
            eh_casa_sobreloja=True)
        casa151 = self.casa.make(
            eh_para_venda=True,
            eh_casa_sobreloja=True)
        apto150A = self.apartamento.make(
            eh_para_venda=True)

        # Quando
        resultado = Imovel.objects_geral.por_tipo_imovel(Imovel.TIPO_IMOVEL.casa).eh("casa_sobreloja")

        # É esperado
        assert len(resultado) == 2
        assert casa150 and casa151 in resultado
        assert apto150A not in resultado

    def test_lista_imovel_eh_casa_terrea(self):
        # Dado
        casa150 = self.casa.make(
            eh_para_venda=True,
            eh_casa_terrea=True)
        casa151 = self.casa.make(
            eh_para_venda=True,
            eh_casa_terrea=True)
        apto150A = self.apartamento.make(
            eh_para_venda=True)

        # Quando
        resultado = Imovel.objects_geral.por_tipo_imovel(Imovel.TIPO_IMOVEL.casa).eh("casa_terrea")

        # É esperado
        assert len(resultado) == 2
        assert casa150 and casa151 in resultado
        assert apto150A not in resultado

    def test_lista_imovel_eh_apto_duplex(self):
        # Dado
        apto150 = self.apartamento.make(
            eh_para_venda=True,
            eh_apto_duplex=True)
        apto151 = self.apartamento.make(
            eh_para_venda=True,
            eh_apto_duplex=False)
        casa150A = self.casa.make(
            eh_para_venda=True)

        # Quando
        resultado = Imovel.objects_geral.por_tipo_imovel(Imovel.TIPO_IMOVEL.apartamento).eh("apto_duplex")

        # É esperado
        assert len(resultado) == 1
        assert apto150 in resultado
        assert casa150A and apto151 not in resultado

    def test_lista_imovel_eh_apto_triplex(self):
        # Dado
        apto150 = self.apartamento.make(
            eh_para_venda=True,
            eh_apto_triplex=True)
        apto151 = self.apartamento.make(
            eh_para_venda=True,
            eh_apto_triplex=True)
        casa150A = self.casa.make(
            eh_para_venda=True)

        # Quando
        resultado = Imovel.objects_geral.por_tipo_imovel(Imovel.TIPO_IMOVEL.apartamento).eh("apto_triplex")

        # É esperado
        assert len(resultado) == 2
        assert apto150 and apto151 in resultado
        assert casa150A not in resultado

    def test_lista_imovel_eh_apto_cobertura(self):
        # Dado
        apto150 = self.apartamento.make(
            eh_para_venda=True,
            eh_apto_cobertura=True)
        apto151 = self.apartamento.make(
            eh_para_venda=True,
            eh_apto_cobertura=True)
        casa150A = self.casa.make(
            eh_para_venda=True)

        # Quando
        resultado = Imovel.objects_geral.por_tipo_imovel(Imovel.TIPO_IMOVEL.apartamento).eh("apto_cobertura")

        # É esperado
        assert len(resultado) == 2
        assert apto150 and apto151 in resultado
        assert casa150A not in resultado

    def test_lista_casa_em_condominio(self):
        # Dado
        condominio = self.condominio.make()
        casa_em_condominio = self.casa.make(
            condominio=condominio)
        casa = self.casa.make()

        # Quando
        resultado = Imovel.objects_geral.em_condominio()

        # É esperado
        assert casa_em_condominio in resultado
        assert casa not in resultado

    def test_lista_imovel_por_bairro(self):
        # Dado
        bairro = self.bairro.make()
        casa = self.casa.make(bairro=bairro)

        # Quando
        resultado = Imovel.objects_geral.por_bairro(bairro)

        # É esperado
        assert casa in resultado
        assert len(resultado) == 1

    def test_lista_imovel_por_bairros(self):
        # Dado
        bairro_1 = self.bairro.make()
        bairro_2 = self.bairro.make()
        bairro_3 = self.bairro.make()
        casa_1 = self.casa.make(bairro=bairro_1)
        casa_2 = self.casa.make(bairro=bairro_2)
        casa_3 = self.casa.make(bairro=bairro_3)

        # Quando
        resultado = Imovel.objects_geral.por_bairros([bairro_1, bairro_2])
        resultado_id = Imovel.objects_geral.por_bairros([bairro_1.id, bairro_2.id])

        # É esperado
        assert casa_1 and casa_2 in resultado and resultado_id
        assert casa_3 not in resultado and resultado_id
        assert len(resultado) and len(resultado_id) == 2

    def test_lista_imoveis_por_min_dormitorio(self):
        # Dado
        apto150A = self.apartamento.make(
            eh_para_venda=True,
            valor_venda=300000,
            dormitorios=3,
            complemento='Apto 150A', )
        apto90A = self.apartamento.make(
            eh_para_venda=True,
            valor_venda=260000,
            dormitorios=2,
            complemento='Apto 90A', )
        apto14A = self.apartamento.make(
            eh_para_venda=True,
            valor_venda=240000,
            dormitorios=1,
            complemento='Apto 14A', )

        # Quando
        resultado = Imovel.para_venda.por_min_dormitorio(1)

        # É esperado
        assert len(resultado) == 3
        assert apto14A and apto90A and apto150A in resultado

    def test_incrementar_codigo_referencia(self):
        """
        O codigo de referencia (imovel_ref) deve ser incremental,
        pegando o útimo + 1
          ex: 2010, 2011, 2012 ...
        """
        casa = self.casa.make()
        assert casa.imovel_ref == "1"

        nova_casa = self.casa.make()
        assert nova_casa.imovel_ref == "2"

        import time
        time.sleep(1)
        novo_apartamento = self.apartamento.make(
            imovel_ref='10')
        assert novo_apartamento.imovel_ref == "10"

        outro_apartamento = self.apartamento.make()
        assert outro_apartamento.imovel_ref == "11"

    def test_lista_imoveis_por_imovel_referencia(self):
        # Dado
        uma_casa = self.casa.make(imovel_ref='1')
        um_apartamento = self.apartamento.make(imovel_ref='2')
        outra_casa = self.apartamento.make(imovel_ref='3')

        # Quando
        resultado = Imovel.objects_geral.por_imovel_referencia('1')

        # É esperado
        assert len(resultado) == 1
        assert uma_casa.imovel_ref == "1"
        assert um_apartamento.imovel_ref == "2"
        assert outra_casa.imovel_ref == "3"
        assert uma_casa in resultado
        assert um_apartamento not in resultado
        assert outra_casa not in resultado

    def test_lista_imoveis_minimo_2_dormitorio_e_bairro(self):
        # Dado
        bairro = self.bairro.make(nome='Centro')
        casa150 = self.casa.make(
            eh_para_venda=True,
            valor_venda=300000,
            dormitorios=3,
            complemento='Apto 150A', )
        apto90A = self.apartamento.make(
            eh_para_venda=True,
            valor_venda=260000,
            dormitorios=2,
            complemento='Apto 90A',
            bairro=bairro
        )

        # Quando
        resultado = Imovel.objects_geral.por_min_dormitorio(2).por_bairro(bairro)

        # É Esperado
        assert len(resultado) == 1
        assert apto90A in resultado

    def test_lista_imoveis_maximo_2_dormitorio_e_bairro(self):
        # Dado
        bairro = self.bairro.make()
        casa150 = self.casa.make(
            eh_para_venda=True,
            valor_venda=300000,
            dormitorios=2,
            complemento='Apto 150A',
            bairro=bairro)
        apto90A = self.apartamento.make(
            eh_para_venda=True,
            valor_venda=260000,
            dormitorios=4,
            complemento='Apto 90A',
        bairro=bairro)

        # Quando
        resultado = Imovel.objects_geral.por_max_dormitorio(2).por_bairro(bairro)

        # É esperado
        assert len(resultado) == 1
        assert casa150 in resultado
        assert apto90A not in resultado

    def test_lista_imoveis_minimo_e_maximo_2_dormitorio(self):
        # Dado
        casa150 = self.casa.make(
            eh_para_venda=True,
            valor_venda=300000,
            dormitorios=3,
            complemento='Apto 150A', )
        apto90A = self.apartamento.make(
            eh_para_venda=True,
            valor_venda=260000,
            dormitorios=2,
            complemento='Apto 90A',
        )
        apto91A = self.apartamento.make(
            eh_para_venda=True,
            valor_venda=260000,
            dormitorios=1,
            complemento='Apto 90A',
        )

        # Quando
        resultado = Imovel.objects_geral.por_min_dormitorio(2).por_max_dormitorio(3)

        # É esperado
        assert len(resultado) == 2
        assert apto90A and casa150 in resultado
        assert apto91A not in resultado

    def test_lista_imovel_com_placa(self):
        # Dado
        casa_com_placa = self.casa.make(esta_com_placa=True)
        casa = self.casa.make()

        # Quando
        resultado = Imovel.objects_geral.com_placa()

        # É esperado
        assert casa_com_placa in resultado
        assert casa not in resultado
        assert len(resultado) == 1

    def test_ordenar_imoveis_menor_valor_venda(self):
        # Dado
        casa_1 = self.casa.make(valor_venda=15.00, eh_para_venda=True)
        casa_2 = self.casa.make(valor_venda=20.00, eh_para_venda=True)
        casa_3 = self.casa.make(valor_venda=10.00, eh_para_venda=True)

        # Quando
        resultado = Imovel.para_venda.ordenar_por_menor_valor()

        # É esperado
        assert casa_3 == resultado[0]
        assert casa_1 == resultado[1]
        assert casa_2 == resultado[2]

    def test_ordenar_imoveis_menor_valor_locacao(self):
        # Dado
        casa_1 = self.casa.make(valor_locacao=15.00,
                                valor_condominio=1.00,
                                eh_para_locacao=True)
        casa_2 = self.casa.make(valor_locacao=20.00,
                                valor_condominio=2.00,
                                eh_para_locacao=True)
        casa_3 = self.casa.make(valor_locacao=10.00,
                                valor_condominio=7.00,
                                eh_para_locacao=True)

        # Quando
        resultado = Imovel.para_locacao.ordenar_por_menor_valor()

        # É esperado
        assert casa_1 == resultado[0]
        assert casa_3 == resultado[1]
        assert casa_2 == resultado[2]

    def test_ordenar_imoveis_venda_por_valor_menor_metro_quadrado(self):
        # Dado
        casa_1 = self.casa.make(valor_venda=15.00,
                                area_construida=1.00,
                                eh_para_venda=True)
        casa_2 = self.casa.make(valor_venda=20.00,
                                area_construida=2.00,
                                eh_para_venda=True)
        casa_3 = self.casa.make(valor_venda=10.00,
                                area_construida=7.00,
                                eh_para_venda=True)

        # Quando
        resultado = Imovel.para_venda.ordenar_por_menor_valor_metro_quadrado()

        # É esperado
        assert casa_3 == resultado[0]
        assert casa_2 == resultado[1]
        assert casa_1 == resultado[2]

    def test_ordenar_imoveis_por_maior_area(self):
        # Dado
        casa_1 = self.casa.make(area_construida=3.00)
        casa_2 = self.casa.make(area_construida=1.00)
        casa_3 = self.casa.make(area_construida=7.00)

        # Quando
        resultado = Imovel.objects_geral.ordenar_por_maior_area()

        # É esperado
        assert casa_3 == resultado[0]
        assert casa_1 == resultado[1]
        assert casa_2 == resultado[2]

    def test_lista_imoveis_por_cidade_nome_simples(self):
        # Dado
        macae = self.cidade.make(nome="Macaé")
        casa_macae = self.casa.make(cidade=macae)
        casa_sao_jose = self.casa.make()

        # Quando
        resultado = Imovel.objects_geral.por_cidade("Macaé")

        # É Esperado
        assert casa_macae in resultado
        assert casa_sao_jose not in resultado

    def test_lista_imoveis_por_cidade_nome_composto(self):
        # Dado
        macae = self.cidade.make(nome="Macaé")
        casa_macae = self.casa.make(cidade=macae)
        casa_sao_jose = self.casa.make()

        # Quando
        resultado = Imovel.objects_geral.por_cidade("São José dos Campos")

        # É Esperado
        assert casa_macae not in resultado
        assert casa_sao_jose  in resultado

    def test_lista_imoveis_mobiliado(self):
        # Dado
        casa_mobiliada = self.casa.make(esta_mobiliado=True)
        casa = self.casa.make()

        # Quando
        resultado = Imovel.objects_geral.esta_mobiliado()

        # É Esperado
        assert casa not in resultado
        assert casa_mobiliada  in resultado

    def test_lista_imoveis_nao_mobiliado(self):
        # Dado
        casa_mobiliada = self.casa.make(esta_mobiliado=True)
        casa = self.casa.make()

        # Quando
        resultado = Imovel.objects_geral.nao_mobiliado()

        # É Esperado
        assert casa in resultado
        assert casa_mobiliada not in resultado

    def test_lista_comercial_para_locacao(self):

        casa_1 = self.casa.make(
            status='publicado',
            eh_para_locacao=True,
            valor_locacao=1500.00,
            eh_comercial=True)

        loja = self.casa.make(
            status='publicado',
            tipo_imovel='loja',
            eh_para_locacao=True,
            valor_locacao=2500.00,
            eh_comercial=True)

        apto_1 = self.apartamento.make(
            status='publicado',
            eh_para_locacao=True,
            valor_locacao=1500.00)

        apto_2 = self.apartamento.make(
            status='publicado',
            eh_para_locacao=True,
            valor_locacao=1500.00)

        # Quando
        resultado = Imovel.para_locacao.publicados().comercial()

        # É Esperado
        assert len(resultado) == 2
        assert casa_1, loja in resultado
        assert apto_1, apto_2 not in resultado

    def test_lista_residencial_para_locacao(self):

        casa_1 = self.casa.make(
            status='publicado',
            eh_para_locacao=True,
            valor_locacao=1500.00,
            eh_comercial=False)

        loja = self.casa.make(
            status='publicado',
            tipo_imovel='loja',
            eh_para_locacao=True,
            valor_locacao=2500.00,
            eh_comercial=True)

        # Quando
        resultado = Imovel.para_locacao.publicados().residencial()

        # É Esperado
        assert len(resultado) == 1
        assert casa_1 in resultado
        assert loja not in resultado
