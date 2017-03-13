# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.db import models


class PropertyListQueryset(models.query.QuerySet):

    def por_referencia(self, referencia):
        referencia = "00%s" % referencia
        return self.filter(listing_id__endswith=referencia)

    def para_alugar(self):
        return self.filter(
            transaction_type='For Rent', archived=False)

    def para_comprar(self):
        return self.filter(
            transaction_type='For Sale', archived=False)

    def por_valor_max(self, valor):
        valor = int(valor*1.10)
        return self.filter(list_price__lte=valor,
                           rental_price__lte=valor)

    def por_tipo_imovel(self, tipo):
        if tipo == 'casa':
            property_type = 'Home'
        elif tipo == 'apartamento':
            property_type = 'Apartment'
        elif tipo == 'comercial':
            property_type = 'Commercial'
        else:
            property_type = 'Land'
        return self.filter(
            property_type__contains=property_type)


class PropertyListManager(models.Manager):

    def get_queryset(self):
        return PropertyListQueryset(self.model, using=self._db)

    def por_referencia(self, referencia):
        return self.get_queryset().por_referencia(referencia)

    def para_alugar(self):
        return self.get_queryset().para_alugar().order_by(
            'city', 'neighborhood', '-rental_price')

    def para_comprar(self):
        return self.get_queryset().para_comprar().order_by(
            'city', 'neighborhood', '-list_price')

    def por_valor_max(self, valor):
        return self.get_queryset().por_valor_max(valor)

    def por_tipo_imovel(self, tipo):
        return self.get_queryset().por_tipo_imovel(tipo)
