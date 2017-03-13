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
Corretor = models.get_model('imobiliaria', 'Corretor')


class Command(BaseCommand):

    """

    Importa os condominios da base legada que foram exportados atraves
    do comando:

      $ ./manage.py dumpdata --indent=2 legado.ImoveisCorretores > captadores.json

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

        usuarios = {0: Corretor.objects.get(pk=2),
                    1: Corretor.objects.get(pk=9),     # Juliana
                    2: Corretor.objects.get(pk=2),     # Verci
                    3: Corretor.objects.get(pk=3),     # ladisman
                    4: Corretor.objects.get(pk=10),     # Simone
                    5: Corretor.objects.get(pk=11),     # Jose
                    6: Corretor.objects.get(pk=12),     # Silvia
                    7: Corretor.objects.get(pk=13),     # Marcos
                    8: Corretor.objects.get(pk=14),     # Juliano
                    9: Corretor.objects.get(pk=1),     # Jorge
                    10: Corretor.objects.get(pk=15),    # Josimar Lima
                    11: Corretor.objects.get(pk=4),    # carlos
                    12: Corretor.objects.get(pk=5),    # Cecilia
                    13: Corretor.objects.get(pk=4),    # Maria
                    15: Corretor.objects.get(pk=2),    # roger
                    16: Corretor.objects.get(pk=2),    # Edson
                    17: Corretor.objects.get(pk=6),    # Odilon Alberto
                    18: Corretor.objects.get(pk=7),    # Elaine
                    19: Corretor.objects.get(pk=8), }  # Valter

        erro = False
        with open(filename, 'rb') as data_file:
            data = json.load(data_file)
            for row in data:
                idcorretor = row['fields'][u'idcorretor']
                idimovel = row['fields'][u'idimovel']

                try:
                    imovel = Imovel.objects.get(
                        imovel_ref=str(idimovel))
                except:
                    imovel = None

                if imovel:

                    if idcorretor not in usuarios:
                        print "[02] Erro buscando usuario: {0}", idcorretor
                        erro = True
                        break

                    user = usuarios.get(idcorretor)

                    try:
                        captador = imovel.corretores.get(pk=user.id)
                        updated_count += 1
                    except:
                        captador = None

                    if not captador:
                        try:
                            imovel.corretores.add(user)
                            created_count += 1
                        except:
                            print "--> Erro ao adicionar corretor: {0}:{1}".format(
                                imovel.imovel_ref, user)
                            erro = True
                            break

                    print "Gravando imovel: ", idimovel
                else:
                    print "Erro buscando imovel: {0}", idimovel

        if not erro:
            self.stdout.write('Created: %s\n' % created_count)
            self.stdout.write('Updated: %s\n' % updated_count)

        self.stdout.write('done\n')
