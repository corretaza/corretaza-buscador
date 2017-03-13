# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.db import models
from django.db.models import Q


class ImovelQueryset(models.query.QuerySet):

    def publicados(self):
        return self.filter(status='publicado')

    def novos(self):
        return self.filter(status='novo').order_by('-id')

    def arquivados(self):
        return self.filter(status='arquivado')

    def por_tipo_imovel(self, tipo_imovel):
        return self.filter(tipo_imovel=tipo_imovel)

    def por_min_dormitorio(self, min):
        return self.filter(dormitorios__gte=min)

    def por_max_dormitorio(self, max):
        return self.filter(dormitorios__lte=max)

    def por_min_vagas_garagem(self, min):
        return self.filter(vagas_garagem__gte=min)

    def por_min_area_construida(self, min):
        return self.filter(area_construida__gte=min)

    def por_bairro(self, bairro):
        return self.filter(bairro=bairro)

    def por_bairros(self, bairro_id_list):
        return self.filter(bairro__in=bairro_id_list)

    def por_imovel_referencia(self, referencia):
        if type(referencia) is not list:
            referencia = [referencia]
        return self.filter(imovel_ref__in=referencia)

    def eh(self, subtipo, value=True):
        key = "eh_{}".format(subtipo)
        condicao = {key:value}
        return self.filter(**condicao)

    def em_condominio(self):
        return self.filter(condominio__isnull=False)

    def por_condominio(self, condominio_id_list):
        if not isinstance(condominio_id_list, list):
            condominio_id_list = [condominio_id_list]
        return self.filter(condominio__in=condominio_id_list)

    def com_placa(self):
        return self.filter(esta_com_placa=True)

    def ordenar_por_maior_area(self):
        return self.all().order_by('-area_construida')

    def por_cidade(self, cidade):
        return self.filter(cidade__nome=cidade)

    def esta_mobiliado(self):
        return self.filter(esta_mobiliado=True)

    def nao_mobiliado(self):
        return self.filter(esta_mobiliado=False)

    def comercial(self):
        return self.filter(eh_comercial=True)

    def residencial(self):
        return self.filter(eh_comercial=False)

    def por_imovel_ref(self, imovel_ref_list):
        imovel_ref_list = imovel_ref_list.upper()
        imovel_ref_list = imovel_ref_list.replace("REF", "")
        imovel_ref_list = imovel_ref_list.replace(";", ",")
        imovel_ref_list = imovel_ref_list.replace(" ", ",")
        imovel_ref_list = imovel_ref_list.split(",")
        return self.filter(imovel_ref__in=imovel_ref_list)

    def por_endereco(self, palavras):
        if not palavras or ',' not in palavras:
            palavras = ''
        lista_palavras = palavras.split(',')
        rua_e_numero = len(lista_palavras) == 2
        rua_numero_e_complemento = len(lista_palavras) == 3
        qs = self.filter(logradouro__icontains=palavras)

        if rua_e_numero:
            qs = self.filter(
                Q(logradouro__icontains=lista_palavras[0]) |
                Q(numero__icontains=lista_palavras[1]) )

        elif rua_numero_e_complemento:
            qs = self.filter(
                Q(logradouro__icontains=lista_palavras[0]) |
                Q(numero__icontains=lista_palavras[1]) |
                Q(complemento__icontains=lista_palavras[2]))
        return qs

    def por_palavras(self, palavras):
        if not palavras:
            palavras = ''

        if 'REF' in palavras.upper():
            return self.por_imovel_ref(palavras)

        if ',' in palavras:
            return self.por_endereco(palavras)

        if palavras.isdigit():
            qs = self.filter(
                Q(cep__icontains=palavras) |
                Q(numero__icontains=palavras) |
                Q(complemento__icontains=palavras))
        else:
            qs = self.filter(
                Q(logradouro__icontains=palavras) |
                Q(bairro__nome__icontains=palavras) |
                Q(condominio__nome__icontains=palavras) |
                Q(proprietario__nome__icontains=palavras) |
                Q(proprietario__nome_conjuge__icontains=palavras))
        return qs


class ImovelQuerysetVenda(ImovelQueryset):

    def por_valor_min(self, min):
        return self.filter(valor_venda__gte=min)

    def por_valor_max(self, max):
        return self.filter(valor_venda__lte=max)

    def ordenar_por_menor_valor(self):
        return self.all().order_by('valor_venda')

    def ordenar_por_menor_valor_metro_quadrado(self):
        return sorted(self.all(),
                      key=lambda imovel: imovel.media_metro_quadrado)


class ImovelQuerysetLocacao(ImovelQueryset):

    def por_valor_min(self, min):
        return self.filter(valor_locacao__gte=min)

    def por_valor_max(self, max):
        return self.filter(valor_locacao__lte=max)

    def ordenar_por_menor_valor(self):
        return sorted(self.all(),
                      key=lambda imovel: imovel.valor_locacao_total)


class ImovelManagerBase(models.Manager):

    def get_queryset(self):
        return ImovelQueryset(self.model, using=self._db)

    def publicados(self):
        return self.get_queryset().publicados()

    def novos(self):
        return self.get_queryset().novos()

    def arquivados(self):
        return self.get_queryset().arquivados()

    def por_tipo_imovel(self, tipo_imovel):
        return self.get_queryset().por_tipo_imovel(tipo_imovel)

    def por_min_dormitorio(self, min):
        return self.get_queryset().por_min_dormitorio(min)

    def por_max_dormitorio(self, max):
        return self.get_queryset().por_max_dormitorio(max)

    def por_min_vagas_garagem(self, min):
        return self.get_queryset().por_min_vagas_garagem(min)

    def por_min_area_construida(self, min):
        return self.get_queryset().por_min_area_construida(min)

    def por_bairro(self, bairro):
        return self.get_queryset().por_bairro(bairro)

    def por_bairros(self, bairro_id_list):
        return self.get_queryset().por_bairros(bairro_id_list)

    def por_imovel_referencia(self, referencia):
        return self.get_queryset().por_imovel_referencia(referencia)

    def eh(self, subtipo):
        return self.get_queryset().eh(subtipo)

    def em_condominio(self):
        return self.get_queryset().em_condominio()

    def por_condominio(self, condominio_id_list):
        return self.get_queryset().por_condominio(condominio_id_list)

    def com_placa(self):
        return self.get_queryset().com_placa()

    def ordenar_por_maior_area(self):
        return self.get_queryset().ordenar_por_maior_area()

    def por_cidade(self, cidade):
        return self.get_queryset().por_cidade(cidade)

    def esta_mobiliado(self):
        return self.get_queryset().esta_mobiliado()

    def nao_mobiliado(self):
        return self.get_queryset().nao_mobiliado()

    def comercial(self):
        return self.get_queryset().comercial()

    def residencial(self):
        return self.get_queryset().residencial()

    def por_palavras(self, palavras):
        return self.get_queryset().por_palavras(palavras)


class ImovelVendasManager(ImovelManagerBase):

    def get_queryset(self, **kwargs):
        queryset = ImovelQuerysetVenda(self.model, using=self._db)
        queryset = queryset.filter(eh_para_venda=True, **kwargs)
        return queryset

    def ordenar_por_menor_valor(self):
        return self.get_queryset().ordenar_por_menor_valor()

    def por_valor_min(self, min):
        return self.get_queryset().por_valor_min(min)

    def por_valor_max(self, max):
        return self.get_queryset().por_valor_max(max)

    def ordenar_por_menor_valor_metro_quadrado(self):
        return self.get_queryset().ordenar_por_menor_valor_metro_quadrado()


class ImovelLocacoesManager(ImovelManagerBase):

    def get_queryset(self, **kwargs):
        queryset = ImovelQuerysetLocacao(self.model, using=self._db)
        queryset = queryset.filter(eh_para_locacao=True, **kwargs)
        return queryset

    def ordenar_por_menor_valor(self):
        return self.get_queryset().ordenar_por_menor_valor()

    def por_valor_min(self, min):
        return self.get_queryset().por_valor_min(min)

    def por_valor_max(self, max):
        return self.get_queryset().por_valor_max(max)
