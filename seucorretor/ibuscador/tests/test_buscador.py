# -*- coding: utf-8 -*-
from django.test.testcases import TestCase
from model_mommy import mommy
from ..models import Imovel
from recipes import criar_dependencia_recipe_imovel


class BuscaTest(object):

    def setUp(self):
        criar_dependencia_recipe_imovel(self)
        self.apartamento_publicado = self.apartamento_base.make(status=Imovel.STATUS.publicado,
                                                                eh_para_locacao=True,
                                                                eh_para_venda=True)
        self.apartamento_novo = self.apartamento_base.make(status=Imovel.STATUS.novo,
                                                           eh_para_locacao=True,
                                                           eh_para_venda=True)
        self.apartamento_arquivado = self.apartamento_base.make(status=Imovel.STATUS.arquivado,
                                                                eh_para_locacao=True,
                                                                eh_para_venda=True)

    def test_get(self):
        self.assertEquals(200, self.response.status_code)

    def _login_usuario(self):
        self.usuario = mommy.make("auth.User",
                                  username="usuario",
                                  password="1234")
        self.usuario.set_password("1234")
        self.usuario.save()
        self.client.login(username=self.usuario.username, password="1234")

    def _assert_listar_somente_imovel_publicado_para_visitantes(self):
        """Listar somente imoveis publicados para os visitantes
        mesmo utilizando o parâmetro arquivado na busca"""
        view = self.response.context_data['view']
        self.assertIn(self.apartamento_publicado, view.get_queryset())
        self.assertNotIn(self.apartamento_arquivado and self.apartamento_novo,
                         view.get_queryset())

    def _assert_listar_imovel_arquivado_para_usuario_logado(self):
        view = self.response.context_data['view']
        self.assertIn(self.apartamento_arquivado, view.get_queryset())
        self.assertNotIn(self.apartamento_publicado and self.apartamento_novo,
                         view.get_queryset())

    def test_listar_somente_imovel_publicado(self):
        self.assertIn(self.apartamento_publicado, self.view.get_queryset())
        self.assertNotIn(self.apartamento_arquivado and self.apartamento_novo,
                         self.view.get_queryset())


class BuscarImovelComprarTest(BuscaTest, TestCase):

    def setUp(self):
        super(BuscarImovelComprarTest, self).setUp()
        self.url_base = '/buscador/comprar/apartamento/cidade/Sao Jose dos Campos/residencial/?codigo_referencia='
        self.response = self.client.get(self.url_base)
        self.view = self.response.context_data['view']

    def test_template(self):
        self.assertTemplateUsed(
            self.response, 'ibuscador/listadeimoveis_comprar_apartamento.html')

    def test_lista_somente_imoveis_a_venda(self):
        apartamento_venda = self.apartamento_base.make(status=Imovel.STATUS.publicado,
                                                       eh_para_venda=True)
        apartamento_locacao = self.apartamento_base.make(status=Imovel.STATUS.publicado,
                                                         eh_para_locacao=True)
        self.assertIn(apartamento_venda, self.view.get_queryset())
        self.assertNotIn(apartamento_locacao, self.view.get_queryset())

    def test_listar_somente_imovel_publicado_para_visitantes(self):
        self.response = self.client.get('{}?status=arquivado'.format(self.url_base))
        self._assert_listar_somente_imovel_publicado_para_visitantes()

    def test_listar_imovel_arquivado_para_usuario_logado(self):
        self._login_usuario()
        self.response = self.client.get('{}&status=arquivado'.format(self.url_base))
        self._assert_listar_imovel_arquivado_para_usuario_logado()

    def test_listar_imoveis_sao_jose(self):
        macae = self.cidade.make(nome="Macae")
        apartamento_macae = self.apartamento_base.make(cidade=macae,
                                                       eh_para_venda=True,
                                                       status=Imovel.STATUS.publicado)
        apartamento_sao_jose = self.apartamento_base.make(eh_para_venda=True,
                                                          status=Imovel.STATUS.publicado)
        self.assertIn(apartamento_sao_jose, self.view.get_queryset())
        self.assertNotIn(apartamento_macae, self.view.get_queryset())


class BuscarImovelAlugarTest(BuscaTest, TestCase):

    def setUp(self):
        super(BuscarImovelAlugarTest, self).setUp()
        self.url_base = '/buscador/alugar/apartamento/cidade/Sao Jose dos Campos/residencial/?codigo_referencia='
        self.response = self.client.get(self.url_base)
        self.view = self.response.context_data['view']

    def test_template(self):
        self.assertTemplateUsed(
            self.response, 'ibuscador/listadeimoveis_alugar_apartamento.html')

    def test_lista_somente_imoveis_para_locacao(self):
        apartamento_venda = self.apartamento_base.make(status=Imovel.STATUS.publicado,
                                                       eh_para_venda=True)
        apartamento_locacao = self.apartamento_base.make(status=Imovel.STATUS.publicado,
                                                         eh_para_locacao=True)
        self.assertIn(apartamento_locacao, self.view.get_queryset())
        self.assertNotIn(apartamento_venda, self.view.get_queryset())

    def test_listar_somente_imovel_publicado_para_visitantes(self):
        self.response = self.client.get('{}?status=arquivado'.format(self.url_base))
        self._assert_listar_somente_imovel_publicado_para_visitantes()

    def test_listar_imovel_arquivado_para_usuario_logado(self):
        self._login_usuario()
        self.response = self.client.get('{}&status=arquivado'.format(self.url_base))
        self._assert_listar_imovel_arquivado_para_usuario_logado()

    def test_listar_imoveis_sao_jose(self):
        macae = self.cidade.make(nome="Macae")
        apartamento_macae = self.apartamento_base.make(cidade=macae,
                                                       eh_para_locacao=True,
                                                       status=Imovel.STATUS.publicado)
        apartamento_sao_jose = self.apartamento_base.make(eh_para_locacao=True,
                                                          status=Imovel.STATUS.publicado)
        self.assertIn(apartamento_sao_jose, self.view.get_queryset())
        self.assertNotIn(apartamento_macae, self.view.get_queryset())


class BuscarApartamentoTest(TestCase):
    def setUp(self):
        criar_dependencia_recipe_imovel(self)
        self.apto_cobertura = self.apartamento_base.make(status=Imovel.STATUS.publicado,
                                                         eh_para_locacao=True,
                                                         eh_apto_cobertura=True,
                                                         esta_mobiliado=True)
        self.apto_duplex = self.apartamento_base.make(status=Imovel.STATUS.publicado,
                                                      eh_para_locacao=True,
                                                      eh_apto_duplex=True)
        self.apto_triplex = self.apartamento_base.make(status=Imovel.STATUS.publicado,
                                                       eh_para_locacao=True,
                                                       eh_apto_triplex=True,
                                                       esta_mobiliado=True)
        self.url_base = '/buscador/alugar/apartamento/cidade/Sao Jose dos Campos/residencial/'
        self.parameter_get = "?valor_min=0&valor_max=0&min_quarto=0&min_vaga=0" \
                             "&area_min=0&mobiliado=&status=publicado&codigo_referencia="

    def test_busca_por_cobertura(self):
        self.response = self.client.get('{}{}&mais_filtros=cobertura'.format(self.url_base,
                                                                             self.parameter_get))
        view = self.response.context_data['view']
        self.assertEquals(len(view.get_queryset()), 1)
        self.assertIn(self.apto_cobertura, view.get_queryset())
        self.assertNotIn(self.apto_duplex and self.apto_triplex,
                         view.get_queryset())

    def test_busca_por_normal(self):
        self.response = self.client.get('{}{}&mais_filtros=normal'.format(self.url_base,
                                                                          self.parameter_get))
        view = self.response.context_data['view']
        self.assertEquals(len(view.get_queryset()), 2)
        self.assertIn(self.apto_duplex and self.apto_triplex, view.get_queryset())
        self.assertNotIn(self.apto_cobertura, view.get_queryset())

    def test_busca_por_convencional(self):
        self.response = self.client.get('{}{}&mais_filtros=convencional'.format(self.url_base,
                                                                                self.parameter_get))
        view = self.response.context_data['view']
        self.assertEquals(len(view.get_queryset()), 1)
        self.assertIn(self.apto_cobertura, view.get_queryset())
        self.assertNotIn(self.apto_duplex and self.apto_triplex,
                         view.get_queryset())

    def test_busca_por_duplex(self):
        self.response = self.client.get('{}{}&mais_filtros=duplex'.format(self.url_base,
                                                                          self.parameter_get))
        view = self.response.context_data['view']
        self.assertEquals(len(view.get_queryset()), 1)
        self.assertIn(self.apto_duplex, view.get_queryset())
        self.assertNotIn(self.apto_cobertura and self.apto_triplex,
                         view.get_queryset())

    def test_busca_por_triplex(self):
        self.response = self.client.get('{}{}&mais_filtros=triplex'.format(self.url_base,
                                                                           self.parameter_get))
        view = self.response.context_data['view']
        self.assertEquals(len(view.get_queryset()), 1)
        self.assertIn(self.apto_triplex, view.get_queryset())
        self.assertNotIn(self.apto_cobertura and self.apto_duplex,
                         view.get_queryset())

    def test_busca_por_cobertura_e_triplex(self):
        self.apto_triplex_cobertura = self.apartamento_base.make(status=Imovel.STATUS.publicado,
                                                                 eh_para_locacao=True,
                                                                 eh_apto_triplex=True,
                                                                 eh_apto_cobertura=True)
        self.response = self.client.get('{}{}&mais_filtros=cobertura&'
                                        'mais_filtros=triplex'.format(self.url_base,
                                                                      self.parameter_get))
        view = self.response.context_data['view']
        self.assertEquals(len(view.get_queryset()), 1)
        self.assertIn(self.apto_triplex_cobertura, view.get_queryset())
        self.assertNotIn(self.apto_cobertura and self.apto_duplex and self.apto_triplex,
                         view.get_queryset())

    def test_busca_por_apartamento_mobiliado(self):
        self.response = self.client.get('{}{}&mais_filtros=mobiliado'.format(self.url_base,
                                                                             self.parameter_get))
        query = self.response.context_data['view'].get_queryset()
        self.assertIn(self.apto_cobertura, query)
        self.assertIn(self.apto_triplex, query)
        self.assertEquals(len(query), 2)
        self.assertNotIn(self.apto_duplex, query)

    def test_busca_por_apartamento_nao_mobiliado(self):
        self.response = self.client.get('{}{}&mais_filtros=nao_mobiliado'.format(self.url_base,
                                                                                 self.parameter_get))
        query = self.response.context_data['view'].get_queryset()
        self.assertNotIn(self.apto_cobertura, query)
        self.assertNotIn(self.apto_triplex, query)
        self.assertEquals(len(query), 1)
        self.assertIn(self.apto_duplex, query)

    def test_busca_por_apartamento_indiferente_mobiliado(self):
        self.response = self.client.get('{}{}&mais_filtros='.format(self.url_base, self.parameter_get))
        query = self.response.context_data['view'].get_queryset()
        self.assertIn(self.apto_cobertura, query)
        self.assertIn(self.apto_triplex, query)
        self.assertIn(self.apto_duplex, query)
        self.assertEquals(len(query), 3)


class BuscarCasaTest(TestCase):
    def setUp(self):
        criar_dependencia_recipe_imovel(self)
        self.casa_terrea = self.casa.make(status=Imovel.STATUS.publicado,
                                          eh_para_locacao=True,
                                          eh_casa_terrea=True,
                                          esta_mobiliado=True)
        self.casa_edicula = self.casa.make(status=Imovel.STATUS.publicado,
                                           eh_para_locacao=True,
                                           eh_casa_edicula=True)
        self.casa_sobreloja = self.casa.make(status=Imovel.STATUS.publicado,
                                             eh_para_locacao=True,
                                             eh_casa_sobreloja=True,
                                             esta_mobiliado=True)
        self.casa_sobrado = self.casa.make(status=Imovel.STATUS.publicado,
                                           eh_para_locacao=True,
                                           eh_casa_sobrado=True)
        self.casa_geminada = self.casa.make(status=Imovel.STATUS.publicado,
                                           eh_para_locacao=True,
                                           eh_casa_geminada=True)
        self.casa_kitnet = self.casa.make(status=Imovel.STATUS.publicado,
                                           eh_para_locacao=True,
                                           eh_kitnet=True)

        self.total_imoveis = 6

        self.url_base = '/buscador/alugar/casa/cidade/Sao Jose dos Campos/residencial/'
        self.parameter_get = "?valor_min=0&valor_max=0&min_quarto=0&min_vaga=0" \
                             "&area_min=0&mobiliado=&status=publicado&codigo_referencia="

    def test_busca_por_terrea(self):
        self.response = self.client.get('{}{}&mais_filtros=terrea'.format(self.url_base,
                                                                          self.parameter_get))
        view = self.response.context_data['view']
        self.assertEquals(len(view.get_queryset()), 1)
        self.assertIn(self.casa_terrea, view.get_queryset())
        self.assertNotIn(self.casa_edicula and self.casa_sobreloja and self.casa_sobrado,
                         view.get_queryset())

    def test_busca_por_edicula(self):
        self.response = self.client.get('{}{}&mais_filtros=edicula'.format(self.url_base,
                                                                          self.parameter_get))
        view = self.response.context_data['view']
        self.assertEquals(len(view.get_queryset()), 1)
        self.assertIn(self.casa_edicula, view.get_queryset())
        self.assertNotIn(self.casa_terrea and self.casa_sobreloja and self.casa_sobrado,
                         view.get_queryset())

    def test_busca_por_sobreloja(self):
        self.response = self.client.get('{}{}&mais_filtros=sobreloja'.format(self.url_base,
                                                                          self.parameter_get))
        view = self.response.context_data['view']
        self.assertEquals(len(view.get_queryset()), 1)
        self.assertIn(self.casa_sobreloja, view.get_queryset())
        self.assertNotIn(self.casa_edicula and self.casa_terrea and self.casa_sobrado,
                         view.get_queryset())

    def test_busca_por_sobrado(self):
        self.response = self.client.get('{}{}&mais_filtros=sobrado'.format(self.url_base,
                                                                           self.parameter_get))
        view = self.response.context_data['view']
        self.assertEquals(len(view.get_queryset()), 1)
        self.assertIn(self.casa_sobrado, view.get_queryset())
        self.assertNotIn(self.casa_edicula and self.casa_sobreloja and self.casa_terrea,
                         view.get_queryset())

    def test_busca_por_geminada(self):
        self.response = self.client.get('{}{}&mais_filtros=geminada'.format(self.url_base,
                                                                           self.parameter_get))
        view = self.response.context_data['view']
        self.assertEquals(len(view.get_queryset()), 1)
        self.assertIn(self.casa_geminada, view.get_queryset())
        self.assertNotIn(self.casa_edicula and self.casa_sobreloja and self.casa_terrea,
                         view.get_queryset())
        self.assertNotIn(self.casa_sobrado, view.get_queryset())

    def test_busca_por_kitnet(self):
        self.response = self.client.get('{}{}&mais_filtros=casa_kitnet'.format(self.url_base,
                                                                           self.parameter_get))
        view = self.response.context_data['view']
        self.assertEquals(len(view.get_queryset()), 1)
        self.assertIn(self.casa_kitnet, view.get_queryset())
        self.assertEquals(len(view.get_queryset()), 1)

    def test_busca_por_terrea_e_sobrado(self):
        casa_terrea_sobrado = self.casa.make(status=Imovel.STATUS.publicado,
                                                  eh_para_locacao=True,
                                                  eh_casa_terrea=True,
                                                  eh_casa_sobrado=True)
        self.response = self.client.get('{}{}&mais_filtros=terrea&'
                                        'mais_filtros=sobrado'.format(self.url_base,
                                                                      self.parameter_get))
        view = self.response.context_data['view']
        self.assertEquals(len(view.get_queryset()), 1)
        self.assertIn(casa_terrea_sobrado, view.get_queryset())
        self.assertNotIn(self.casa_terrea and
                         self.casa_edicula and
                         self.casa_sobreloja and
                         self.casa_sobrado,
                         view.get_queryset())

    def test_busca_por_casa_mobiliada(self):
        self.response = self.client.get('{}{}&mais_filtros=mobiliado'.format(self.url_base,
                                                                             self.parameter_get))
        query = self.response.context_data['view'].get_queryset()
        self.assertIn(self.casa_terrea, query)
        self.assertIn(self.casa_sobreloja, query)
        self.assertEquals(len(query), 2)
        self.assertNotIn(self.casa_edicula, query)
        self.assertNotIn(self.casa_sobrado, query)

    def test_busca_por_casa_nao_mobiliada(self):
        self.response = self.client.get('{}{}&mais_filtros=nao_mobiliado'.format(self.url_base,
                                                                                 self.parameter_get))
        query = self.response.context_data['view'].get_queryset()
        self.assertNotIn(self.casa_terrea, query)
        self.assertNotIn(self.casa_sobreloja, query)
        terrea_e_sobreloja = 2
        self.assertEquals(len(query), self.total_imoveis-terrea_e_sobreloja)
        self.assertIn(self.casa_edicula, query)
        self.assertIn(self.casa_sobrado, query)

    def test_busca_por_casa_indiferente_mobiliada(self):
        self.response = self.client.get('{}{}&mais_filtros='.format(self.url_base,
                                                                    self.parameter_get))
        query = self.response.context_data['view'].get_queryset()
        self.assertIn(self.casa_terrea, query)
        self.assertIn(self.casa_sobreloja, query)
        self.assertIn(self.casa_edicula, query)
        self.assertIn(self.casa_sobrado, query)
        self.assertEquals(len(query), self.total_imoveis)
