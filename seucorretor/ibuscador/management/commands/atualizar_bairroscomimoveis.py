# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.core.management.base import BaseCommand
from django.db import models

Bairro = models.get_model('cidades', 'Bairro')
BairroComImoveis = models.get_model('ibuscador', 'BairroComImoveis')
Imovel = models.get_model('ibuscador', 'Imovel')


class Command(BaseCommand):

    help = "Atualiza o total de imoveis (venda/compra) por bairro. Deve ser executado apenas 1 vez"

    def handle(self, *args, **options):

        tipos = ['apartamento', 'casa', 'terreno', 'areaurbana',
                 'chacara', 'loja', 'sala', 'galpao']
        for tipo in tipos:
            for bairro in Bairro.objects.all():
                contador_venda = Imovel.para_venda.publicados().por_tipo_imovel(
                    tipo).por_bairro(bairro).count()
                contador_locacao = Imovel.para_locacao.publicados().por_tipo_imovel(
                    tipo).por_bairro(bairro).count()
                contador, created = BairroComImoveis.objects.get_or_create(
                    bairro=bairro, tipo_imovel=tipo)
                contador.cidade = bairro.cidade
                contador.regiao = bairro.regiao
                contador.contador_venda = contador_venda
                contador.contador_locacao = contador_locacao
                contador.save()
                print "... ", bairro.nome

        self.stdout.write('done\n')
