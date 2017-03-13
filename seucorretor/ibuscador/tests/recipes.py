# -*- coding: UTF-8 -*-
from model_mommy.recipe import Recipe, foreign_key
from cidades.models import Cidade, Regiao, Bairro
from ..models import Imovel, Condominio
from crm.models import Proprietario


def criar_dependencia_recipe_imovel(instance):
    instance.cidade = Recipe(Cidade,
                             nome='Sao Jose dos Campos')
    instance.regiao = Recipe(Regiao,
                             nome='Oeste',
                             cidade=foreign_key(instance.cidade))
    instance.bairro = Recipe(Bairro,
                             nome='Aquarius',
                             regiao=foreign_key(instance.regiao))
    instance.proprietario = Recipe(Proprietario,
                                   nome='Roger Waters',
                                   fone='12998001002')
    instance.condominio = Recipe(Condominio,
                                 cep='12120000',
                                 logradouro='Rua Tubarão Branco',
                                 numero='900',
                                 bairro=foreign_key(instance.bairro),
                                 regiao=foreign_key(instance.regiao),
                                 cidade=foreign_key(instance.cidade))
    instance.apartamento_base = Recipe(Imovel,
                                       proprietario=foreign_key(
                                           instance.proprietario),
                                       tipo_imovel=Imovel.TIPO_IMOVEL.apartamento,
                                       dormitorios=2,
                                       cidade=foreign_key(instance.cidade),
                                       bairro=foreign_key(instance.bairro),
                                       complemento='Apto 14A')
    instance.casa = Recipe(Imovel,
                           proprietario=foreign_key(instance.proprietario),
                           tipo_imovel=Imovel.TIPO_IMOVEL.casa,
                           dormitorios=3,
                           cidade=foreign_key(instance.cidade),
                           bairro=foreign_key(instance.bairro))
