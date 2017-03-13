# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.db import models
from django.utils.translation import ugettext_lazy as _

from ibuscador.models import Imovel
from .managers import PropertyListManager


class PropertyList(models.Model):
    """
    Usado para IMPORTAR o arquivo XML da viva real gerado por sites EXTERNOS a 
    nossa plataforma.

    IMPORTANTE:
    - Este model será descontinuado em BREVE (@deprecated)
    - Este model é valido para imobiliarias que usam os PAINEIS,
    e não iram fazer uso modulo BUSCADOR (ou seja já possuem um site e
    pretendem continuar com o mesmo)
    """

    listing_id = models.CharField(max_length=32)
    transaction_type = models.CharField(max_length=16)
    featured = models.BooleanField(default=False)
    property_type = models.CharField(max_length=128, blank=True)
    description = models.TextField(max_length=1024, blank=True)
    list_price = models.IntegerField(default=0, blank=True)
    rental_price = models.IntegerField(default=0, blank=True)
    property_administration_fee = models.IntegerField(default=0, blank=True)
    bedrooms = models.IntegerField(default=0, blank=True)
    bathrooms = models.IntegerField(default=0, blank=True)
    garage = models.IntegerField(default=0, blank=True)
    constructed_area = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00)
    country = models.CharField(max_length=64, blank=True)
    state = models.CharField(max_length=8, blank=True)
    city = models.CharField(max_length=64, blank=True)
    neighborhood = models.CharField(max_length=128, blank=True)
    postal_code = models.CharField(max_length=16, blank=True)
    archived = models.BooleanField(default=False)
    new = models.BooleanField(default=True)

    objects = PropertyListManager()

    def __unicode__(self):
        return self.listing_id

    @property
    def price_verbose(self):
        return self.rental_price if self.transaction_type == 'For Rent' else self.list_price

    @property
    def imovel_ref(self):
        return str(int(self.listing_id))

    @property
    def imovel_url(self):
        return "http://sjcvaleimoveis.com.br/temp/imovel.php?imovel={0}".format(
            self.imovel_ref)


class Media(models.Model):
    property_list = models.ForeignKey(PropertyList, verbose_name=_('property'))
    item = models.CharField(max_length=512)


class ImovelVivaReal(Imovel):
    """
    Usado para gerar arquivo XML para viva real (EXPORTAR)
    ver http://manual.vivareal.com/home
    """
    class Meta:
        proxy = True

    @property
    def tipo_transacao(self):
        if self.eh_para_venda and self.eh_para_locacao:
            return 'Sale/Rent'
        elif self.eh_para_locacao:
            return 'For Rent'
        else:
            return 'For Sale'

    @property
    def titulo_verbose(self):
        if self.tipo_imovel == ImovelVivaReal.TIPO_IMOVEL.terreno or \
           self.tipo_imovel == ImovelVivaReal.TIPO_IMOVEL.chacara or \
           self.tipo_imovel == ImovelVivaReal.TIPO_IMOVEL.areaurbana:
            return "{0}, {1}m^2".format(self.titulo, self.area_terreno)

        elif self.tipo_imovel == ImovelVivaReal.TIPO_IMOVEL.casa or \
             self.tipo_imovel == ImovelVivaReal.TIPO_IMOVEL.apartamento:
            return "{0}, {1} dorm.".format(self.titulo, self.dormitorios)

        elif self.tipo_imovel == ImovelVivaReal.TIPO_IMOVEL.loja or \
             self.tipo_imovel == ImovelVivaReal.TIPO_IMOVEL.sala:
            return "{0}, {1} sala(s)".format(self.titulo, self.dormitorios)

        elif self.tipo_imovel == ImovelVivaReal.TIPO_IMOVEL.galpao or \
             self.tipo_imovel == ImovelVivaReal.TIPO_IMOVEL.edificio:
            return "{0}, {1}m^2".format(self.titulo, self.area_construida)
        else:
            return self.titulo

    @property
    def destaque(self):
        """ Hoje o padrão é não ser destaque
        ver ticket: #75
        """
        return False

    @property
    def tipo_imovel_vivareal(self):

        if self.eh_comercial:
            # Commercial / Consultorio
            # Commercial / Business
            if self.tipo_imovel == ImovelVivaReal.TIPO_IMOVEL.apartamento:
                return 'Commercial / Building'
            elif self.tipo_imovel == ImovelVivaReal.TIPO_IMOVEL.casa:
                return 'Commercial / Building'
            elif self.tipo_imovel == ImovelVivaReal.TIPO_IMOVEL.terreno:
                return 'Commercial / Land Lot'
            elif self.tipo_imovel == ImovelVivaReal.TIPO_IMOVEL.areaurbana:
                return 'Commercial / Land Lot'
            elif self.tipo_imovel == ImovelVivaReal.TIPO_IMOVEL.chacara:
                return 'Commercial / Agricultural'
            elif self.tipo_imovel == ImovelVivaReal.TIPO_IMOVEL.loja:
                return 'Commercial / Loja'
            elif self.tipo_imovel == ImovelVivaReal.TIPO_IMOVEL.sala:
                return 'Commercial / Office'
            elif self.tipo_imovel == ImovelVivaReal.TIPO_IMOVEL.galpao:
                return 'Commercial / Industrial'
            elif self.tipo_imovel == ImovelVivaReal.TIPO_IMOVEL.edificio:
                return 'Commercial / Residential Income'
        else:

            if self.tipo_imovel == ImovelVivaReal.TIPO_IMOVEL.apartamento:
                return 'Residential / Apartment'
            elif self.tipo_imovel == ImovelVivaReal.TIPO_IMOVEL.casa:
                # Residential / Flat
                # Residential / Penthouse
                # Residential / Kitnet
                if self.eh_casa_sobrado:
                    return 'Residential / Sobrado'
                if self.condominio:
                    return 'Residential / Condo'
                else:
                    return 'Residential / Home'
            elif self.tipo_imovel == ImovelVivaReal.TIPO_IMOVEL.terreno:
                return 'Residential / Land Lot'
            elif self.tipo_imovel == ImovelVivaReal.TIPO_IMOVEL.areaurbana:
                return 'Residential / Land Lot'
            elif self.tipo_imovel == ImovelVivaReal.TIPO_IMOVEL.chacara:
                return 'Residential / Farm Ranch'
            elif self.tipo_imovel == ImovelVivaReal.TIPO_IMOVEL.chacara:
                return 'Residential / Farm Ranch'
            else:
                return 'Residential / Home'

    @property
    def tags(self):
        tags = ""
        for tag in filter(lambda metodo:metodo.startswith("_tag"), dir(self)):
            tags += getattr(self, tag)()
        return tags.replace("><", ">\n<")

    @property
    def tipo_endereco(self):
        if self.numero:
            return "Street"
        return "Neighborhood"

    @property
    def descricao_imovel_vivareal(self):
        return self.descricao_imovel.replace("\n", " &lt;br&gt;")

    def _tags_tipo_imovel(self):
        """
        Regras conforme:
        --> http://manual.vivareal.com/3-3-regras-de-validacao
        """
        tags = ''
        # Dormitorios
        mostrar_dorm = [Imovel.TIPO_IMOVEL.apartamento,
                        Imovel.TIPO_IMOVEL.casa,
                        Imovel.TIPO_IMOVEL.chacara, ]
        if self.tipo_imovel in mostrar_dorm:
            tags += "<Bedrooms>{}</Bedrooms>\n".format(self.dormitorios)

        # Banheiros
        nao_mostrar_banheiro = self.eh_terreno or self.eh_edificio
        if not nao_mostrar_banheiro:
            tags += "<Bathrooms>{}</Bathrooms>\n".format(self.banheiros)
            tags += "<Suites>{}</Suites>\n".format(self.suites_verbose)

        # Garagem
        if self.vagas_garagem:
            tags += "<Garage>{}</Garage>\n".format(self.vagas_garagem)

        # Area
        if self.tem_area_total:
            tags += '<LotArea unit="square metres">{}</LotArea>'.format(self.area_total)
        else:
            tags += '<LivingArea unit="square metres">{}</LivingArea>'.format(self.area_total)

        if self.eh_para_venda:
            tags += '<ListPrice currency="BRL">{}</ListPrice>'.format(
                int(self.valor_venda))
        if self.eh_para_locacao:
            tags += '<RentalPrice currency="BRL" period="Monthly">{}</RentalPrice>'.format(
                int(self.valor_locacao))

        tags += '<PropertyAdministrationFee currency="BRL">{}</PropertyAdministrationFee>'.format(
            int(self.valor_condominio))
        return tags

    def _tag_descricao(self):
        return '<Description><![CDATA[{}]]></Description>'.format(
            self.descricao_imovel_vivareal)
