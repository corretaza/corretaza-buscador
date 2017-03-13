# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

import urllib
import base64

from os.path import basename
from datetime import datetime
from optparse import make_option

from django.db import models
from django.utils.encoding import smart_str
from django.core.files import File
from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.conf import settings

from suds.client import Client

ImovelZapImovel = models.get_model('zapimoveis', 'ImovelZapImovel')


def gera_xml(imoveis_list, filename):
    """
    Gera arquivo XML com os imóveis
    """
    context = {'data': datetime.today(),
               'imoveis': imoveis_list,
               'domain': Site.objects.get_current(), }

    content = render_to_string(
        'zapimoveis/xml_base.xml', context)

    with open(filename, 'w') as xml:
        xml.write(content.encode('utf-8'))


def envia_xml_para_zapimoveis(target_xml, user, password):
    """
    Envia o XML convertido para base64 para o WS da Zap Imoveis
    """
    url = 'http://ws.zap.com.br/EnvArqSenha.asmx?wsdl'
    client = Client(url)
    print client

    with open(target_xml) as xmlfile:
        encodedxml = base64.b64encode(xmlfile.read())

    #print encodedxml
    client.service.AtualizarArquivo(user, password, encodedxml)


class Command(BaseCommand):
    """
    O objectivo deste comando é ler o arquivo XML da viva real e importar as FOTOS
    para atualizar o novo cadastro de imoveis
    """
    help = "Create the nginx file"
    option_list = BaseCommand.option_list + (
        make_option('--imoveis', action='store', dest='imoveis', type="int",
                    help='Quantidade de imoveis para enviar'),
    )

    def handle(self, *args, **options):
        """ """
        qtd_imoveis = options['imoveis']
        if not qtd_imoveis:
            qtd_imoveis = 2

        imoveis_list = ImovelZapImovel.objects_geral.publicados().order_by(
            '-atualizado_em')[:qtd_imoveis]

        target_xml = '{0}/zapfile.xml'.format(settings.MEDIA_ROOT)

        gera_xml(imoveis_list, target_xml)

        envia_xml_para_zapimoveis(target_xml, "2450408", "0371956")

        for imovel in imoveis_list:
            self.stdout.write(imovel.imovel_ref)

        self.stdout.write('done\n')
