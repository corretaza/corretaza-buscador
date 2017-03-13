# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

import json

from optparse import make_option

from django.core.management.base import BaseCommand
from django.db import models

Condominio = models.get_model('ibuscador', 'Condominio')
AreaDeLazer = models.get_model('ibuscador', 'AreaDeLazer')
Bairro = models.get_model('cidades', 'Bairro')


class Command(BaseCommand):

    """

    Importa os condominios da base legada que foram exportados atraves 
    do comando:

      $ ./manage.py dumpdata --indent=2 legado.Edificio > edificio.json

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

        created_count = 0
        updated_count = 0
        condominio_count = 0

        with open(filename, 'rb') as data_file:
            data = json.load(data_file)

            for row in data:
                nome = row['fields'][u'descricao'].title()
                construtora = row['fields']['construtora'].title()
                ano_construcao = row['fields']['data_construcao']
                tem_elevador = False
                if row['fields']['tem_elevador'] == 'S':
                    tem_elevador = True
                nro_andares = int(row['fields']['andar'])
                logradouro = row['fields']['endereco'].title()
                numero = row['fields']['numero']
                id_bairro = row['fields']['idbairro']
                ids_arealazer = row['fields']['arealazer']

                bairro = None
                try:
                    bairro = Bairro.objects.get(id=id_bairro)
                except:
                    if not id_bairro:
                        print "--> Bairro inválido para: {0} ({1})".format(
                          nome, row['pk'])
                    else:
                        print "--> Bairro não encontrado para: {0} ({1}) - bairro: {2}".format(
                            nome, row['pk'], id_bairro)

                condominio, created = Condominio.objects.get_or_create(
                    pk=int(row['pk']))
                condominio.nome = nome
                condominio.construtora = construtora
                if ano_construcao:
                    condominio.ano_construcao = int(ano_construcao[:4])
                condominio.tem_elevador = tem_elevador
                condominio.andares = nro_andares

                condominio.logradouro = logradouro
                condominio.numero = numero
                if bairro:
                    condominio.bairro = bairro
                    condominio.regiao = bairro.regiao
                    condominio.cidade = bairro.cidade

                condominio.save()

                if ids_arealazer:
                    for id_alazer in ids_arealazer.split(';'):
                        try:
                            # arealazer = AreaDeLazer.objects.get(id=id_alazer)
                            # condominio.areadelazer_condominio.get_or_create(pk=id_alazer)
                            arealazer = condominio.areadelazer_condominio.get(pk=id_alazer)
                        except:
                            arealazer = None

                        if not arealazer:
                            try:
                                arealazer = AreaDeLazer.objects.get(id=id_alazer)
                                condominio.areadelazer_condominio.add(arealazer)
                                condominio_count += 1

                            except Exception as e:
                                print "--> Area de lazer não encontrado: {0} {1}, {2})".format(
                                    id_alazer, nome,e)

                if created:
                    created_count += 1
                else:
                    updated_count += 1

        self.stdout.write('Created: %s\n' % created_count)
        self.stdout.write('Updated: %s\n' % updated_count)
        self.stdout.write('Area lazer added: %s\n' % condominio_count)

        self.stdout.write('done\n')
