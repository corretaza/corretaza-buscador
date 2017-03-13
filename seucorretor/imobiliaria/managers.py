# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.db import models
from django.db.models import Q


class ColaboradorQueryset(models.query.QuerySet):

    def ativos(self):
        return self.filter(is_ativo=True)


class ColaboradorManager(models.Manager):

    def get_queryset(self):
        return ColaboradorQueryset(self.model, using=self._db)

    def ativos(self):
        return self.get_queryset().ativos()


class CorretorQueryset(models.query.QuerySet):

    def todos(self):
        qs = self.filter(is_ativo=True)
        return qs.order_by('nome')

    def com_menos_atendimentos(self, tipo_interesse):
        qs = self.filter(is_ativo=True)
        return qs.order_by('pausado', '{0}_contador'.format(tipo_interesse))

    def com_pouco_na_fila(self, tipo_interesse, contador):
        """
           Lista os corretores com o indicador de fila < contador
           Usado para nivelar os atendimentos, ou seja, aquele corretor
           que ficou pausado por semanas nao receber todos atendimentos novos
           (uma vez que seu indicador de fila estaria baixo)
        """
        if tipo_interesse == 'comprar':
            qs = self.filter(is_ativo=True, pausado=True,
                             comprar_contador__lt=contador)
        else:
            qs = self.filter(is_ativo=True, pausado=True,
                             alugar_contador__lt=contador)
        return qs

    def ativos(self):
        return self.filter(is_ativo=True)


class CorretorManager(models.Manager):

    def get_queryset(self):
        return CorretorQueryset(self.model, using=self._db)

    def todos(self):
        return self.get_queryset().todos()

    def com_menos_atendimentos(self, tipo_interesse):
        return self.get_queryset().com_menos_atendimentos(tipo_interesse)

    def com_pouco_na_fila(self, tipo_interesse, contador):
        return self.get_queryset().com_pouco_na_fila(tipo_interesse, contador)

    def ativos(self):
        return self.get_queryset().ativos()
