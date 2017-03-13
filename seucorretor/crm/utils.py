# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

INVALID_PHONE_CHARS = "()-+."


def formata_fone(fone):
    """ retorna o numero de telefone visualmente melhor para leitura """
    if len(fone) == 11:
        return "(%s) %s %s-%s" % (fone[:2], fone[2:3], fone[3:7], fone[7:])
    elif len(fone) == 10:
        return "(%s) %s-%s" % (fone[:2], fone[2:6], fone[6:])
    else:
        return fone


def formata_fone_limpa(fone):
    """ remove caracteres nao numericos do fone """
    if fone == '(00)0000-0000':
        return ''
    if not fone:
        return ''
    fone = "".join(fone.split())
    for digit in INVALID_PHONE_CHARS:
        fone = fone.replace(digit, "")
    if not fone.isdigit():
        fone = ''
    return fone
