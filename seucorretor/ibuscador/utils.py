# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Imovel


def imovel_ref_valida(imovel_ref):
    """ Usado para validar se uma dada referencia eh valida """
    imoveis = Imovel.objects_geral.publicados().por_imovel_referencia(imovel_ref)
    if not imoveis:
        return False
    return True


def ordernar_query(queryset, ordem):
    def _try_get_ordem(queryset, query):
        try:
            return getattr(queryset, query).__call__()
        except AttributeError:
            return queryset.ordenar_por_menor_valor()
    metodos_ordenacao = {'custo_m_quadrado':
                         _try_get_ordem(queryset,
                                        "ordenar_por_menor_valor_metro_quadrado"),
                         'maior_area': queryset.ordenar_por_maior_area()}
    return metodos_ordenacao.get(ordem, queryset.ordenar_por_menor_valor())


def monta_queryset_com_filtros_da_pesquisa(queryset, fields, tipo_imovel):

    valor_min = fields.get('valor_min')
    if valor_min and int(float(valor_min)) > 0:
        queryset = queryset.por_valor_min(valor_min)

    valor_max = fields.get('valor_max')
    if valor_max and int(float(valor_max)) > 0:
        queryset = queryset.por_valor_max(valor_max)

    min_quarto = fields.get('min_quarto')
    if min_quarto and int(min_quarto) > 0:
        queryset = queryset.por_min_dormitorio(min_quarto)

    min_vaga = fields.get('min_vaga')
    if min_vaga and int(min_vaga) > 0:
        queryset = queryset.por_min_vagas_garagem(min_vaga)

    area_min = fields.get('area_min')
    if area_min and int(float(area_min)) > 0:
        queryset = queryset.por_min_area_construida(area_min)

    bairros = fields.getlist('bairros')
    if bairros:
        bairros_ids = [int(id) for id in bairros]
        queryset = queryset.por_bairros(bairros_ids)

    em_condominio = fields.get('em_condominio')
    if em_condominio: #condominio fechado
        queryset = queryset.em_condominio()

    condominio = fields.get('condominio')
    if condominio and condominio[0]:
        queryset = queryset.por_condominio(int(condominio))

    filtro = filtrar_por_tipo_imovel(tipo_imovel)
    if filtro:
        for tipo in fields.getlist('mais_filtros'):
            queryset = filtro(queryset, tipo)
        queryset = filtro(queryset, fields.get('mobiliado'))

    codigo_referencia = fields.get("codigo_referencia")
    if codigo_referencia:
        codigos = [codigo.strip() for codigo in codigo_referencia.split(",")]
        queryset = queryset.por_imovel_referencia(codigos)
    return queryset


def filtrar_por_tipo_imovel(tipo_imovel):
    tipos_imoveis = {
        'CASA': filtrar_tipo_casa,
        'APARTAMENTO': filtrar_tipo_apartamento
    }
    return tipos_imoveis.get(tipo_imovel.upper(), None)


def filtrar_tipo_apartamento(queryset, tipo):
    tipo_apartamento = {
        'COBERTURA': queryset.eh('apto_cobertura'),
        'NORMAL': queryset.eh('apto_cobertura', False),
        'DUPLEX': queryset.eh('apto_duplex'),
        'TRIPLEX': queryset.eh('apto_triplex'),
        'CONVENCIONAL': queryset.eh('apto_triplex', False).eh('apto_duplex', False),
        'MOBILIADO': queryset.esta_mobiliado(),
        'NAO_MOBILIADO': queryset.nao_mobiliado()
    }
    return tipo_apartamento.get(str(tipo).upper(), queryset)


def filtrar_tipo_casa(queryset, tipo):
    tipo_casa = {
        'TERREA': queryset.eh('casa_terrea'),
        'EDICULA': queryset.eh('casa_edicula'),
        'SOBRELOJA': queryset.eh('casa_sobreloja'),
        'SOBRADO': queryset.eh('casa_sobrado'),
        'MOBILIADO': queryset.esta_mobiliado(),
        'NAO_MOBILIADO': queryset.nao_mobiliado()
    }
    return tipo_casa.get(str(tipo).upper(), queryset)


def validar_query_status_imovel(request, interesse=Imovel.para_venda):
    if request.GET.get('status', "") == "arquivado" and request.user.is_authenticated():
        return interesse.arquivados()
    return interesse.publicados()
