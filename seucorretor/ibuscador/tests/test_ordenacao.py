from django.test.testcases import TestCase
from recipes import criar_dependencia_recipe_imovel
from ..models import Imovel


class OrdenacaoImovelTest(TestCase):

    def setUp(self):
        criar_dependencia_recipe_imovel(self)
        self.apartamento_1 = self.apartamento_base.make(status=Imovel.STATUS.publicado,
                                                   eh_para_venda=True,
                                                   eh_para_locacao=True,
                                                   area_construida=100.00,
                                                   valor_venda=50.00,
                                                   valor_locacao=30.00)
        self.apartamento_2 = self.apartamento_base.make(status=Imovel.STATUS.publicado,
                                                   eh_para_venda=True,
                                                   eh_para_locacao=True,
                                                   area_construida=10.00,
                                                   valor_venda=150.00,
                                                   valor_locacao=10)
        self.apartamento_3 = self.apartamento_base.make(status=Imovel.STATUS.publicado,
                                                   eh_para_venda=True,
                                                   eh_para_locacao=True,
                                                   area_construida=25.00,
                                                   valor_venda=40.00,
                                                   valor_locacao=40)
        self.parameter_get = "?valor_min=0&valor_max=0&min_quarto=0&min_vaga=0" \
                             "&area_min=0&mobiliado=&status=publicado&codigo_referencia="

    def test_ordernar_maior_area(self):
        response = self.client.get(
            '/buscador/comprar/apartamento/cidade/Sao Jose dos Campos/residencial/{}'
            '&ordenar_por=maior_area'.format(self.parameter_get))
        query_set = response.context_data['view'].get_queryset()
        self.assertEquals(query_set[0], self.apartamento_1)
        self.assertEquals(query_set[1], self.apartamento_3)
        self.assertEquals(query_set[2], self.apartamento_2)

    def test_ordernar_menor_valor_venda(self):
        response = self.client.get(
            '/buscador/comprar/apartamento/cidade/Sao Jose dos Campos/residencial/{}'
            '&ordenar_por=menor_valor'.format(self.parameter_get))
        query_set = response.context_data['view'].get_queryset()
        self.assertEquals(query_set[0], self.apartamento_3)
        self.assertEquals(query_set[1], self.apartamento_1)
        self.assertEquals(query_set[2], self.apartamento_2)

    def test_ordernar_menor_valor_locacao(self):
        response = self.client.get(
            '/buscador/alugar/apartamento/cidade/Sao Jose dos Campos/residencial/{}'
            '&ordenar_por=menor_valor'.format(self.parameter_get))
        query_set = response.context_data['view'].get_queryset()
        self.assertEquals(query_set[0], self.apartamento_2)
        self.assertEquals(query_set[1], self.apartamento_1)
        self.assertEquals(query_set[2], self.apartamento_3)

    def test_ordernar_venda_menor_custo_m_quarado(self):
        response = self.client.get(
            '/buscador/comprar/apartamento/cidade/Sao Jose dos Campos/residencial/{}'
            '&ordenar_por=custo_m_quadrado'.format(self.parameter_get))
        query_set = response.context_data['view'].get_queryset()
        self.assertEquals(query_set[0], self.apartamento_1)
        self.assertEquals(query_set[1], self.apartamento_3)
        self.assertEquals(query_set[2], self.apartamento_2)

    def test_ordernar_menor_valor_quando_ordem_invalida_selecionada(self):
        response = self.client.get(
            '/buscador/comprar/apartamento/cidade/Sao Jose dos Campos/residencial/{}'
            '&ordenar_por=qualquer'.format(self.parameter_get))
        query_set = response.context_data['view'].get_queryset()
        self.assertEquals(query_set[0], self.apartamento_3)
        self.assertEquals(query_set[1], self.apartamento_1)
        self.assertEquals(query_set[2], self.apartamento_2)

    def test_ordenar_por_id_quando_custo_m_quadrado_em_aluguel(self):
        response = self.client.get(
            '/buscador/alugar/apartamento/cidade/Sao Jose dos Campos/residencial/{}'
            '&ordenar_por=custo_m_quadrado'.format(self.parameter_get))
        query_set = response.context_data['view'].get_queryset()
        self.assertEquals(query_set[0], self.apartamento_2)
        self.assertEquals(query_set[1], self.apartamento_1)
        self.assertEquals(query_set[2], self.apartamento_3)
