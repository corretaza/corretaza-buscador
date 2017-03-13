# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

import urllib
from os.path import basename
from bs4 import BeautifulSoup

from optparse import make_option

from django.utils.encoding import smart_str
from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import models
# from django.utils import timezone

Imovel = models.get_model('ibuscador', 'Imovel')
Foto = models.get_model('ibuscador', 'Foto')


class Command(BaseCommand):
    """
    O objectivo deste comando é ler o arquivo XML da viva real e importar as FOTOS
    para atualizar o novo cadastro de imoveis
    """
    help = "Create the nginx file"
    option_list = BaseCommand.option_list + (
        make_option('--file', action='store', dest='file', type="string",
                    help='Set the CSV file'),
    )

    def handle(self, *args, **options):
        """ """
        filename = options['file']

        created_count = 0
        existing_count = 0

        with open(filename, 'rb') as f:
            handler = f.read().decode('utf-8')
            soup = BeautifulSoup(handler, 'xml')

            for listing in soup.ListingDataFeed.Listings.findAll('Listing'):
                listing_id = listing.find('ListingID').string
                transaction_type = listing.find('TransactionType').string

                featured = False
                try:
                    list_Featured = listing.find('Featured').string
                    if list_Featured == 'true':
                        featured = True
                except:
                    pass

                property_type = listing.find('Details').PropertyType.string
                description = listing.find('Details').Description.string
                list_price = listing.find('Details').ListPrice.string
                rental_price = listing.find('Details').RentalPrice.string

                try:
                    property_administration_fee = listing.find(
                        'Details').PropertyAdministrationFee.string
                except:
                    property_administration_fee = 0

                try:
                    imovel_ref_str = str(int(listing_id))
                    imovel = Imovel.objects.get(imovel_ref=imovel_ref_str)
                    print "got imovel: ", imovel.pk, " (", imovel_ref_str, ")"

                except:
                    imovel = None

                if imovel:

                    if not imovel.fotos_list:
                        try:
                            listing.find('Media').find('Item')
                        except:
                            print "no media for: %s" % listing_id
                            continue

                        foto_count = 1
                        primeira_foto = False
                        for item in listing.find('Media').findAll('Item'):
                            foto_url = item.string
                            # TODO> dar um nome melhor para o arquivo
                            temp_name = 'imovel{0}_foto{1}.jpg'.format(
                                imovel.pk, foto_count)

                            print 'getting {0}'.format(foto_url)
                            foto_from_site = urllib.urlretrieve(foto_url)
                            nova_foto = Foto.objects.create(imovel=imovel)
                            nova_foto.picture.save(
                                basename(foto_url), File(open(foto_from_site[0])))
                            if not primeira_foto:
                                primeira_foto = True
                                nova_foto.eh_principal = primeira_foto

                            nova_foto.save()
                            print "foto inserida {0}".format(nova_foto.id)
                            created_count += 1
                    else:
                        existing_count += 1
                        "Foto existente para {0}".format(listing_id)
                else:
                    print "Imovel {} nao encontrado".format(listing_id)



        self.stdout.write('Created: %s\n' % created_count)
        self.stdout.write('Com fotos existentes: %s\n' % existing_count)
        self.stdout.write('done\n')
