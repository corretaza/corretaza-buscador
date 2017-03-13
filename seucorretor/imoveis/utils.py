# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals


def obtem_campos_alterados(atual, novo):
    """
    Obtem os campos importantes que foram alterados.
    Retorna '' se nada importante foi alterado
    TODO: Ver se a app abaixo resolveria melhor isto aqui:
    --> github.com/grantmcconnaughey/django-field-history
    """
    resultado = ''
    if atual.valor_locacao != novo.valor_locacao:
        resultado += u'Valor locacao alterado de R${0} para R${1}. '.format(
            atual.valor_locacao, novo.valor_locacao)
    if atual.valor_venda != novo.valor_venda:
        resultado += u'Valor venda alterado de R${0} para R${1}. '.format(
            atual.valor_venda, novo.valor_venda)
    if atual.valor_condominio != novo.valor_condominio:
        resultado += u'Valor condominio alterado de R${0} para R${1}. '.format(
            atual.valor_condominio, novo.valor_condominio)
    if atual.proprietario != novo.proprietario:
        resultado += u"Proprietário alterado de '{0}' para '{1}'. ".format(
            atual.proprietario, novo.proprietario)
    if atual.condominio != novo.condominio:
        resultado += u"Condomínio alterado de '{0}' para '{1}'. ".format(
            atual.condominio, novo.condominio)
    end_atualizado = atual.logradouro != novo.logradouro or \
        atual.numero != novo.numero or \
        atual.complemento != novo.complemento or \
        atual.cep != novo.cep
    if end_atualizado:
        resultado += u' Endereço atualizado (antes: {0}, {1} {2} - cep:{3}). '.format(
            atual.logradouro, atual.numero, atual.complemento, atual.cep)
    loc_atualizado = atual.bairro != novo.bairro or \
        atual.regiao != novo.regiao or \
        atual.cidade != novo.cidade
    if loc_atualizado:
        resultado += u' Localização atualizada (antes: {0} - {1} - {2}). '.format(
            atual.bairro, atual.regiao, atual.cidade)
    return resultado
