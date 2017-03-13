from recipes import criar_dependencia_recipe_imovel
from ..models import BairroComImoveis, Imovel, Condominio
from cidades.models import Cidade, Bairro
from ..forms import FiltroPorValorForm
from model_mommy.recipe import Recipe, foreign_key
import pytest

pytestmark = pytest.mark.django_db

@pytest.mark.django_db
class TestForm():

    def setup_method(self, test_method):
        criar_dependencia_recipe_imovel(self)
        self.recipe_bairro_imovel_sj = Recipe(BairroComImoveis,
                                              cidade=foreign_key(self.cidade),
                                              bairro=foreign_key(self.bairro),
                                              regiao=foreign_key(self.regiao),
                                              tipo_imovel=Imovel.TIPO_IMOVEL.apartamento)
        self.cidade_macae = Recipe(Cidade,
                                   nome="Macae")
        self.bairro_aeroporto = Recipe(Bairro,
                                       nome="Aeroporto")
        self.recipe_bairro_imovel_macae = Recipe(BairroComImoveis,
                                                 cidade=foreign_key(self.cidade_macae),
                                                 bairro=foreign_key(self.bairro_aeroporto),
                                                 regiao=foreign_key(self.regiao),
                                                 tipo_imovel=Imovel.TIPO_IMOVEL.apartamento)

    def test_form_bairro_sao_jose_dos_campos(self):
        bairro_imovel_sj = self.recipe_bairro_imovel_sj.make(contador_venda=1)
        bairro_imovel_macae = self.recipe_bairro_imovel_macae.make()
        form = FiltroPorValorForm(tipo_imovel=Imovel.TIPO_IMOVEL.apartamento,
                                  tipo_interesse="comprar",
                                  cidade="Sao Jose dos Campos")
        assert len(form.fields['bairros'].choices) == 1
        assert (bairro_imovel_sj.bairro.id, bairro_imovel_sj) in form.fields['bairros'].choices
        assert (bairro_imovel_macae.bairro.id, bairro_imovel_macae) not in form.fields['bairros'].choices

    def test_form_bairro_macae(self):
        bairro_imovel_sj = self.recipe_bairro_imovel_sj.make()
        bairro_imovel_macae = self.recipe_bairro_imovel_macae.make(contador_venda=1)
        form = FiltroPorValorForm(tipo_imovel=Imovel.TIPO_IMOVEL.apartamento,
                                  tipo_interesse="comprar",
                                  cidade="Macae")
        assert len(form.fields['bairros'].choices) == 1
        assert (bairro_imovel_macae.bairro.id, bairro_imovel_macae) in form.fields['bairros'].choices
        assert (bairro_imovel_sj.bairro.id, bairro_imovel_sj) not in form.fields['bairros'].choices

    def test_form_condominio_macae(self):
        condominio = self.condominio.make()
        form = FiltroPorValorForm(tipo_imovel=Imovel.TIPO_IMOVEL.apartamento,
                                  tipo_interesse="comprar",
                                  cidade="Macae")
        assert len(form.fields['condominio'].choices) == 1
        assert ("", "---------------") in form.fields['condominio'].choices
        assert (condominio.id, condominio.nome) not in form.fields['condominio'].choices

    def test_form_condominio_sj(self):
        condominio = self.condominio.make()
        form = FiltroPorValorForm(tipo_imovel=Imovel.TIPO_IMOVEL.apartamento,
                                  tipo_interesse="comprar",
                                  cidade="Sao Jose dos Campos")
        assert len(form.fields['condominio'].choices) == 2
        assert ("", "---------------") in form.fields['condominio'].choices
        assert (condominio.id, condominio.nome) in form.fields['condominio'].choices


