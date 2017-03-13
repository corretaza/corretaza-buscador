# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

# from datetime import datetime
from bs4 import BeautifulSoup

from optparse import make_option

from django.utils.encoding import smart_str
from django.core.management.base import BaseCommand
from django.db import models
# from django.utils import timezone

PropertyList = models.get_model('vivareal', 'PropertyList')
Media = models.get_model('vivareal', 'Media')


class Command(BaseCommand):
    help = "Create the nginx file"
    option_list = BaseCommand.option_list + (
        make_option('--file', action='store', dest='file', type="string",
                    help='Set the CSV file'),
    )

    def handle(self, *args, **options):
        """ """
        filename = options['file']

        created_count = 0
        updated_count = 0

        PropertyList.objects.all().update(archived=True, new=False)

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

                bedrooms = listing.find('Details').Bedrooms.string
                bathrooms = listing.find('Details').Bathrooms.string
                garage = listing.find('Details').Garage.string
                constructed_area = listing.find(
                    'Details').ConstructedArea.string

                country = listing.find('Location').Country.string
                state = listing.find('Location').State.string
                city = listing.find('Location').City.string
                neighborhood = listing.find('Location').Neighborhood.string
                postal_code = listing.find('Location').PostalCode.string

                new_property, created = PropertyList.objects.get_or_create(
                    listing_id=listing_id)
                new_property.transaction_type = transaction_type
                new_property.featured = featured
                new_property.property_type = property_type

                new_property.description = smart_str(description)
                new_property.list_price = int(list_price)
                new_property.rental_price = int(rental_price)
                new_property.property_administration_fee = int(
                    property_administration_fee)
                new_property.bedrooms = int(bedrooms)
                new_property.bathrooms = int(bathrooms)
                new_property.garage = int(garage)
                new_property.constructed_area = float(constructed_area)

                new_property.country = smart_str(country)
                new_property.state = smart_str(state)
                new_property.city = smart_str(city)
                new_property.neighborhood = smart_str(neighborhood)
                new_property.postal_code = postal_code
                new_property.archived = False

                if created:
                    created_count += 1
                    new_property.new = True
                else:
                    updated_count += 1

                new_property.save()

                try:
                    listing.find('Media').find('Item')
                except:
                    print "no media for: %s" % listing_id
                    continue

                for item in listing.find('Media').findAll('Item'):
                    new_item, created = Media.objects.get_or_create(
                                            property_list=new_property,
                                            item=item.string
                                        )

        self.stdout.write('Created: %s\n' % created_count)
        self.stdout.write('Updated: %s\n' % updated_count)
        self.stdout.write('done\n')
