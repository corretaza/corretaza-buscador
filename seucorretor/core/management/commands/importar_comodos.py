# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

import json

from optparse import make_option
from django.core.management.base import BaseCommand
from django.db import models

Imovel = models.get_model('ibuscador', 'Imovel')
DescricaoComodo = models.get_model('ibuscador', 'DescricaoComodo')


class Command(BaseCommand):

    """

    Importa as caracteristicas dos imoveis (desc. comodos) da base legada que foram exportados atraves 
    do comando:

      $ ./manage.py dumpdata --indent=2 legado.ImoveisCaracteristicas > comodos.json

    """
    help = "Importa os imoveis de um JSON"
    option_list = BaseCommand.option_list + (
        make_option('--file',
                    action='store', dest='file',
                    type="string", help='Set the JSON file'),
    )

    def handle(self, *args, **options):
        """ """
        filename = options['file']
        created_count = 0
        erro1_count = 0
        erro2_count = 0

        with open(filename, 'rb') as data_file:
            data = json.load(data_file)
            for row in data:
                desc_comodo_id = row['fields'][u'item']
                imovel_id = row['fields'][u'idimovel']

                try:

                    imovel = Imovel.objects.get(imovel_ref=str(imovel_id))
                    desccomodo = DescricaoComodo.objects.get(pk=desc_comodo_id)

                except:
                    imovel = None
                    desccomodo = None

                if imovel and desccomodo:
                    if desccomodo.descricao:
                        imovel.descricao_comodos += "\n{0}".format(
                            desccomodo.descricao.title())
                        imovel.save()
                        created_count += 1
                    else:
                        erro1_count += 1
                        print "---> comodo: ", desc_comodo_id

                else:
                    print "Pulando: {0} {1}".format(
                        imovel_id, desc_comodo_id)
                    erro1_count += 2

            self.stdout.write('Created: %s\n' % created_count)
            self.stdout.write('Erro obtendo descricao: %s\n' % erro1_count)
            self.stdout.write('Erro obtendo imovel/comodo: %s\n' % erro2_count)
            self.stdout.write('done\n')
