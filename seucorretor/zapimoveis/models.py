# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.db import models
from django.utils.translation import ugettext_lazy as _

from imobiliaria.behaviours import Preferences
from ibuscador.models import Imovel


class ImovelZapImovel(Imovel):
    """
    Usado para gerar arquivo XML para zap imoveis
    """
    class Meta:
        proxy = True

    @property
    def tipo_oferta(self):
        """
        Conforme o manual de carga do Zap Imoveis:
        1 = Sem destaque
        2 = Destaque
        3 = Super Destaque
        """
        # TODO: Semanalmente definir os X (do plano) em Destaque
        # TODO: Semanalmente desmarcar imoveis super destaque vendidos/nao publicado
        if self.super_destaque_para_portais:
            return 3
        else:
            return 2

    @property
    def tipo_zap(self):
        if self.tipo_imovel == ImovelZapImovel.TIPO_IMOVEL.apartamento:
            return 'Apartamento'
        elif self.tipo_imovel == ImovelZapImovel.TIPO_IMOVEL.casa:
            return 'Casa'
        elif self.tipo_imovel == ImovelZapImovel.TIPO_IMOVEL.terreno:
            return 'Terreno'
        elif self.tipo_imovel == ImovelZapImovel.TIPO_IMOVEL.areaurbana:
            return 'Terreno'
        elif self.tipo_imovel == ImovelZapImovel.TIPO_IMOVEL.chacara:
            return 'Rural'
        elif self.eh_comercial:
            return 'Comercial/Industrial'

    @property
    def subtipo_zap(self):

        if self.tipo_imovel == ImovelZapImovel.TIPO_IMOVEL.apartamento:
            #Apartamento Padrão, Kitchenette/Conjugados, Loft
            return 'Apartamento Padrão'
        elif self.tipo_imovel == ImovelZapImovel.TIPO_IMOVEL.casa:
            #Casa de Condomínio, Casa de Vila, Casa Padrão
            if self.condominio:
                return 'Casa de Condomínio'
            else:
                return 'Casa Padrão'
        elif self.tipo_imovel == ImovelZapImovel.TIPO_IMOVEL.terreno:
            #Terreno Padrão, Loteamento/Condomínio
            if self.condominio:
                return 'Loteamento/Condomínio'
            else:
                return 'Terreno Padrão'

        elif self.tipo_imovel == ImovelZapImovel.TIPO_IMOVEL.areaurbana:
            if self.condominio:
                return 'Loteamento/Condomínio'
            else:
                return 'Terreno Padrão'

        elif self.tipo_imovel == ImovelZapImovel.TIPO_IMOVEL.chacara:
            #Chácara, Sítio, Fazenda, Haras
            return 'Chácara'

        elif self.eh_comercial:
            #Box/Garagem, Loja de Shopping/Centro Comercial, Studio, Hotel, Motel, Pousada/Chalé, Indústria
            if self.tipo_imovel == ImovelZapImovel.TIPO_IMOVEL.edificio:
                return 'Prédio Inteiro'
            elif self.tipo_imovel == ImovelZapImovel.TIPO_IMOVEL.casa:
                return 'Casa Comercial'
            elif self.tipo_imovel == ImovelZapImovel.TIPO_IMOVEL.loja:
                return 'Loja/Salão'
            elif self.tipo_imovel == ImovelZapImovel.TIPO_IMOVEL.galpao:
                return 'Galpão/Depósito/Armazém'
            elif self.tipo_imovel == ImovelZapImovel.TIPO_IMOVEL.sala:
                return 'Conjunto Comercial/sala'

    @property
    def categoria_zap(self):
        if self.eh_apto_cobertura and self.eh_apto_duplex:
            return 'Cobertura Duplex'
        elif self.eh_apto_cobertura and self.eh_apto_triplex:
            return 'Cobertura Tríplex'
        elif self.eh_apto_duplex:
            return 'Duplex'
        elif self.eh_apto_triplex:
            return 'Tríplex'
        elif self.eh_apto_cobertura:
            return 'Cobertura'
        elif self.eh_casa_terrea:
            return 'Térrea'
        elif self.eh_casa_sobrado:
            return 'Sobrado'
        else:
            return 'Padrão'

    @property
    def finalidade(self):
        if self.eh_para_venda and self.eh_para_locacao:
            return 'Venda/Locação'
        elif self.eh_para_locacao:
            return 'Locação'
        else:
            return 'Venda'


class ImovelWeb(Imovel):
    """
    Usado para gerar arquivo XML para zap imoveis
    """
    class Meta:
        proxy = True

    @property
    def destaque(self):
        """ Hoje o padrão é não ser destaque
        ver ticket: #75
        """
        # TODO: retornar corretamente a qtd certa
        # de <Modelo>Especial</Modelo>
        return False

    @property
    def tipo(self):
        if self.tipo_imovel == ImovelZapImovel.TIPO_IMOVEL.apartamento:
            return 'Apartamento'
        elif self.tipo_imovel == ImovelZapImovel.TIPO_IMOVEL.casa:
            return 'Casa'
        elif self.tipo_imovel == ImovelZapImovel.TIPO_IMOVEL.terreno:
            return 'Terreno'
        elif self.tipo_imovel == ImovelZapImovel.TIPO_IMOVEL.areaurbana:
            return 'Terreno'
        elif self.tipo_imovel == ImovelZapImovel.TIPO_IMOVEL.chacara:
            return 'Rural'
        elif self.eh_comercial:
            return 'Comercial'

    @property
    def subtipo(self):

        if self.tipo_imovel == ImovelWeb.TIPO_IMOVEL.apartamento:
            #Padrão, Kitchenette/Studio, Loft ou Flat
            return 'Padrão'
        elif self.tipo_imovel == ImovelWeb.TIPO_IMOVEL.casa:
            #Padrão, Casa de Condomínio, Casa de Vila
            if self.condominio:
                return 'Casa de Condomínio'
            else:
                return 'Padrão'
        elif self.tipo_imovel == ImovelWeb.TIPO_IMOVEL.terreno:
            #Terreno Padrão, Loteamento/Condomínio
            if self.condominio:
                return 'Loteamento/Condomínio'
            else:
                return 'Terreno Padrão'

        elif self.tipo_imovel == ImovelWeb.TIPO_IMOVEL.areaurbana:
            if self.condominio:
                return 'Loteamento/Condomínio'
            else:
                return 'Terreno Padrão'

        elif self.tipo_imovel == ImovelWeb.TIPO_IMOVEL.chacara:
            #Chácara, Sítio, Fazenda, Haras
            return 'Rural'

        elif self.eh_comercial:
            #Box/Garagem, Prédio Inteiro, Conj Comercial/sala,
            #casa comercial, Loja de shopping/centro comercia
            #Loja/Salao, galpao/deposito/armazem
            #hotel motel pousada ou Industria
            if self.tipo_imovel == ImovelWeb.TIPO_IMOVEL.edificio:
                return 'Prédio Inteiro'
            elif self.tipo_imovel == ImovelWeb.TIPO_IMOVEL.casa:
                return 'Casa Comercial'
            elif self.tipo_imovel == ImovelWeb.TIPO_IMOVEL.loja:
                return 'Loja/Salão'
            elif self.tipo_imovel == ImovelWeb.TIPO_IMOVEL.galpao:
                return 'Galpão/Depósito/Armazém'
            elif self.tipo_imovel == ImovelWeb.TIPO_IMOVEL.sala:
                return 'Conjunto Comercial/sala'

    @property
    def categoria(self):
        if self.eh_apto_cobertura and self.eh_apto_duplex:
            return 'Cobertura Duplex'
        elif self.eh_apto_cobertura and self.eh_apto_triplex:
            return 'Cobertura Tríplex'
        elif self.eh_apto_duplex:
            return 'Duplex'
        elif self.eh_apto_triplex:
            return 'Tríplex'
        elif self.eh_apto_cobertura:
            return 'Cobertura'
        elif self.eh_casa_terrea:
            return 'Térrea'
        elif self.eh_casa_sobrado:
            return 'Sobrado'
        else:
            return 'Padrão'


class ImovelOlx(Imovel):
    """
    Usado para gerar arquivo XML para OLX
    """
    class Meta:
        proxy = True

    @property
    def tipo_olx(self):
        if self.tipo_imovel == ImovelOlx.TIPO_IMOVEL.apartamento:
            return 'Apartamento'
        elif self.tipo_imovel == ImovelOlx.TIPO_IMOVEL.casa:
            return 'Casa'
        elif self.tipo_imovel == ImovelOlx.TIPO_IMOVEL.terreno:
            return 'Terreno'
        elif self.tipo_imovel == ImovelOlx.TIPO_IMOVEL.areaurbana:
            return 'Terreno'
        elif self.tipo_imovel == ImovelOlx.TIPO_IMOVEL.chacara:
            return 'Chácara'
        elif self.eh_comercial:
            if self.tipo_imovel == ImovelOlx.TIPO_IMOVEL.edificio:
                return 'Comercial/Industrial'
            elif self.tipo_imovel == ImovelOlx.TIPO_IMOVEL.loja:
                return 'Comercial/Industrial'
            elif self.tipo_imovel == ImovelOlx.TIPO_IMOVEL.galpao:
                return 'Comercial/Industrial'
            elif self.tipo_imovel == ImovelOlx.TIPO_IMOVEL.sala:
                return 'Comercial/Industrial'
            else:
                return 'Comercial'

    @property
    def subtipo_olx(self):

        if self.tipo_imovel == ImovelOlx.TIPO_IMOVEL.apartamento:
            #Loft, Kitchenette/Conjugados, Flat, Kitnet Residencial
            return 'Apartamento Padrão'

        elif self.tipo_imovel == ImovelOlx.TIPO_IMOVEL.casa:
            #Casa de Condomínio, Casa de Vila, Casa Padrão
            if self.condominio:
                return 'Casa de Condomínio'
            else:
                return 'Casa Padrão'
        elif self.tipo_imovel == ImovelOlx.TIPO_IMOVEL.terreno:
            #Terreno Padrão, Loteamento/Condomínio
            if self.condominio:
                return 'Loteamento/Condomínio'
            else:
                return 'Terreno Padrão'

        elif self.tipo_imovel == ImovelOlx.TIPO_IMOVEL.areaurbana:
            if self.condominio:
                return 'Loteamento/Condomínio'
            else:
                return 'Terreno Padrão'

        elif self.tipo_imovel == ImovelOlx.TIPO_IMOVEL.chacara:
            # Sítio​ ​ Rural
            return 'Chácara Rural'

        elif self.eh_comercial:
            # Hotel, Conjunto Comercial/sala, Box/Garagem
            if self.tipo_imovel == ImovelOlx.TIPO_IMOVEL.edificio:
                return 'Prédio Inteiro'
            elif self.tipo_imovel == ImovelOlx.TIPO_IMOVEL.casa:
                return 'Casa Comercial'
            elif self.tipo_imovel == ImovelOlx.TIPO_IMOVEL.loja:
                return 'Loja/Salão'
            elif self.tipo_imovel == ImovelOlx.TIPO_IMOVEL.galpao:
                return 'Galpão/Depósito/Armazém'
            elif self.tipo_imovel == ImovelOlx.TIPO_IMOVEL.sala:
                return 'Conjunto Comercial/sala'

    @property
    def categoria_olx(self):
        if self.eh_apto_cobertura and self.eh_apto_duplex:
            return 'Cobertura Duplex'
        elif self.eh_apto_cobertura and self.eh_apto_triplex:
            return 'Cobertura Triplex'
        elif self.eh_apto_duplex:
            return 'Duplex'
        elif self.eh_apto_triplex:
            return 'Triplex'
        elif self.eh_apto_cobertura:
            return 'Cobertura'
        elif self.eh_casa_terrea:
            return 'Térrea'
        elif self.eh_casa_sobrado:
            return 'Sobrado/Duplex'
        else:
            return 'Padrão'



class ZapPreferences(Preferences):
    """ @see behaviours.Preferences """
    qtd_imoveis_para_exportacao = models.PositiveIntegerField(
        'Quantidade de imóveis para exportar', blank=True, default=100)

    def __unicode__(self):
        return "ZapPreferences"

    class Meta:
        verbose_name = "ZapPreferences"
        verbose_name_plural = "ZapPreferences"
