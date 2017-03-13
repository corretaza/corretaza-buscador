# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

import json

from optparse import make_option
from datetime import datetime

from django.utils import timezone
from django.core.management.base import BaseCommand
from django.db import models

Imovel = models.get_model('ibuscador', 'Imovel')
HistoricoDeImovel = models.get_model('ibuscador', 'HistoricoDeImovel')
User = models.get_model('auth', 'User')


class Command(BaseCommand):

    """

    Importa os condominios da base legada que foram exportados atraves 
    do comando:

      $ ./manage.py dumpdata --indent=2 legado.ImoveisHistorico > imoveishistorico.json

    """
    help = "Importa os condominios de um JSON"
    option_list = BaseCommand.option_list + (
        make_option('--file',
                    action='store', dest='file',
                    type="string", help='Set the JSON file'),
    )

    def handle(self, *args, **options):
        """ """
        filename = options['file']
        usuarios = {}

        created_count = 0
        updated_count = 0
        condominio_count = 0

        usuarios = {
            u'carlos': User.objects.get(username='carlos'),
            u'cecilia': User.objects.get(username='cecilia'),
            u'elaine': User.objects.get(username='elaine'),
            u'jorge': User.objects.get(username='jorge'),
            u'odilon': User.objects.get(username='odilon'),
            u'silvia': User.objects.get(username='silvia'),
            u'verci': User.objects.get(username='verci'),
            u'edson': User.objects.get(username='verci'),
            u'lima': User.objects.get(username='verci'),
            u'marcos': User.objects.get(username='verci'),
            u'assist': User.objects.get(username='verci'),
            u'andressa': User.objects.get(username='verci'),
            u'maria': User.objects.get(username='verci'), }

        erro = False
        with open(filename, 'rb') as data_file:
            data = json.load(data_file)
            for row in data:
                datahora = row['fields'][u'datahora']
                idimovel = row['fields'][u'idimovel']
                usuario = row['fields'][u'usuario'].lower()
                descricao = row['fields'][u'descricao']

                try:
                    imovel = Imovel.objects.get(
                        imovel_ref=str(idimovel))
                except:
                    imovel = None

                if imovel:
                    if usuario not in usuarios:
                        print "[02] Erro buscando usuario: {0}", usuario
                        erro = True
                        break
                    user = usuarios.get(usuario)

                    # convertendo o formato "2014-05-31T17:52:47Z"
                    data_importacao = datetime.strptime(
                        datahora, "%Y-%m-%dT%H:%M:%SZ")

                    HistoricoDeImovel.objects.create(
                        data=data_importacao, imovel=imovel,
                        usuario=user, conteudo=descricao)
                    print "Gravando imovel: ", idimovel
                    created_count += 1
                else:
                    print "Erro buscando imovel: {0}", idimovel

        if not erro:
            self.stdout.write('Created: %s\n' % created_count)

        self.stdout.write('done\n')
