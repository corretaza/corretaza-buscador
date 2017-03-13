# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from datetime import datetime

import json

from optparse import make_option

from django.core.management.base import BaseCommand
from django.db import models
from django.db.models import Q
from django.utils import timezone

Proprietario = models.get_model('crm', 'Proprietario')
Atendimento = models.get_model('crm', 'Atendimento')

INVALID_PHONE_CHARS = "()-+"


def format_phone_number(phone_number):
    """ removes invalid chars from phone numbers """
    if phone_number == '(00)0000-0000':
        return ''
    if not phone_number:
        return ''
    phone_number = "".join(phone_number.split())
    for digit in INVALID_PHONE_CHARS:
        phone_number = phone_number.replace(digit, "")
    return phone_number


class Command(BaseCommand):

    """

    Importa os Proprietarios dabase legada que foram
    exportados atraves do comando:

    $ ./manage.py dumpdata --indent=2 legado.Clientes > proprietarios.json

    Nota:
    deve se apagar todos clientes NAO proprietario
    clist = Clientes.objects.filter(tipo_cliente!=6)

    """

    help = "Create the nginx file"
    option_list = BaseCommand.option_list + (
        make_option(
            '--file', action='store', dest='file', type="string",
            help='Set the CSV file'),
    )

    def handle(self, *args, **options):

        filename = options['file']
        created_count = 0
        updated_count = 0

        with open(filename, 'rb') as data_file:
            data = json.load(data_file)
            for row in data:
                pk = row['pk']
                nome = row['fields'][u'razao_social'].title()
                email = row['fields'][u'email']
                email2 = row['fields'][u'email2']
                if email:
                    email = email.lower()
                    if email.startswith('nt@nt.com'):
                        email = ''
                if email2:
                    email2 = email2.lower()
                else:
                    email2 = ''
                tel1 = format_phone_number(row['fields'][u'tel1'])
                tel2 = format_phone_number(row['fields'][u'tel2'])
                tel3 = format_phone_number(row['fields'][u'cel'])
                tel4 = format_phone_number(row['fields'][u'cel2'])
                data_cadastro = row['fields'][u'data_cadastro']

                if not tel1:
                    if tel2:
                        tel1 = tel2
                        tel2 = ''
                    elif tel3:
                        tel1 = tel3
                        tel3 = ''
                    elif tel4:
                        tel1 = tel4
                        tel4 = ''

                proprietario, created = Proprietario.objects.get_or_create(
                    nome=nome, email=email, fone=tel1)
                proprietario.fone2 = tel2
                proprietario.fone3 = tel3
                proprietario.fone4 = tel4
                proprietario.email_alternativo = email2
                if data_cadastro:
                    proprietario.data_criacao = datetime.strptime(
                        data_cadastro, "%Y-%m-%d").replace(
                        tzinfo=timezone.utc)
                else:
                    proprietario.data_criacao = datetime.now()
                proprietario.id_legado = str(pk)

                atendimento = Atendimento.objects.filter(
                    Q(fone__contains=tel1) |
                    Q(fone2__contains=tel1) |
                    Q(fone3__contains=tel1))

                if not atendimento:
                    atendimento = Atendimento.objects.filter(
                        email__icontains=email)
                if atendimento:
                    proprietario.atendimento = atendimento[0]
                proprietario.save()
                print "{0} ok".format(proprietario.id)

                if created:
                    created_count += 1
                else:
                    updated_count += 1

        self.stdout.write('Created: %s\n' % created_count)
        self.stdout.write('Updated: %s\n' % updated_count)
        self.stdout.write('done\n')
