# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

import json
from datetime import datetime
from optparse import make_option

from django.utils import timezone
from django.core.management.base import BaseCommand
from django.db import models

Proprietario = models.get_model('crm', 'Proprietario')
Imovel = models.get_model('ibuscador', 'Imovel')
Condominio = models.get_model('ibuscador', 'Condominio')
AreaDeLazer = models.get_model('ibuscador', 'AreaDeLazer')
FormaDePagamento = models.get_model('ibuscador', 'FormaDePagamento')
Bairro = models.get_model('cidades', 'Bairro')


def trata_int(valor):
    if not valor:
        return 0
    if type(valor) == int:
        return valor
    if '.' in str(valor):
        return int(valor[:-3])
    return int(valor)


class Command(BaseCommand):

    """

    Importa os imoveis da base legada que foram exportados atraves 
    do comando:

      $ ./manage.py dumpdata --indent=2 legado.Imoveis > imoveis.json

    Antes é necessário:
    1) Alterar o nome dos condominios para TITLE()
       from legado.models import Imoveis
       ilist = Imoveis.objects.all()
       for imovel in ilist:
           if imovel.nomecondominio:
               imovel.nomecondominio = imovel.nomecondominio.title()
           if imovel.edificio:
               imovel.edificio = imovel.edificio.title()
           imovel.save()
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

        erro = False
        created_count = 0
        updated_count = 0
        proprietario_count = 0
        condominio_validar_count = []
        condominio_update_count = 0
        bairro_validar_count = 0
        areas_cond_count = 0
        areas_imovel_count = 0

        try:
            db_fgts = FormaDePagamento.objects.get(
                descricao='FGTS')
        except:
            print "[01] Cadastre a forma de Pgto: FGTS"
            exit

        try:
            db_financiamento = FormaDePagamento.objects.get(
                descricao='Financiamento')
        except:
            print "[01] Cadastre a forma de Pgto: Financiamento"
            exit

        try:
            db_proposta = FormaDePagamento.objects.get(
                descricao='Estuda proposta')
        except:
            print "[01] Cadastre a forma de Pgto: Estuda proposta"
            exit

        try:
            db_imovelmenorvalor = FormaDePagamento.objects.get(
                descricao='Imóvel menor valor')
        except:
            print "[01] Cadastre a forma de Pgto: Im\u00f3vel menor valor"
            exit

        with open(filename, 'rb') as data_file:
            data = json.load(data_file)
            for row in data:
                novo_imovel, created = Imovel.objects.get_or_create(
                    imovel_ref=str(row['pk']))

                novo_imovel.status = 'novo'
                if row['fields'][u'publicar'] == 'S':
                    novo_imovel.status = 'publicado'
                elif row['fields'][u'arquivado'] == 'S':
                    novo_imovel.status = 'arquivado'

                if created:
                    created_count += 1
                else:
                    updated_count += 1

                proprietario_id = row['fields'][u'proprietario']

                try:
                    proprietario = Proprietario.objects.get(
                        id_legado=str(proprietario_id))
                except:
                    proprietario = None

                if not proprietario and novo_imovel.status == 'publicado':
                    print row['pk'], '...'
                    print "[01] Proprietario nao encontrado:", proprietario_id
                    erro = True
                    break

                novo_imovel.proprietario = proprietario

                idedificio = 0
                condominio = None
                if row['fields'][u'idedificio']:
                    idedificio = int(row['fields'][u'idedificio'])

                if idedificio:
                    try:
                        condominio = Condominio.objects.get(pk=idedificio)
                        #if row['fields'][u'edificio']:
                        #    condominio = Condominio.objects.get(
                        #        nome__iexact=row['fields'][u'edificio'])
                        #elif row['fields'][u'nomecondominio']:
                        #    condominio = Condominio.objects.get(
                        #        nome__iexact=row['fields'][u'nomecondominio'])
                        #else:
                    except:
                        try:
                            condominio = Condominio.objects.get(pk=idedificio)
                            if condominio.logradouro.lower() != row['fields'][u'logradouro'].lower():
                                print "    ---> [02] Validar o condominio da ref: ", row['pk'], condominio.nome, '==', row['fields'][u'edificio'] if row['fields'][u'edificio'] else row['fields'][u'nomecondominio']
                                condominio_validar_count.append(row['pk'])
                        except:
                            condominio = None
                            if novo_imovel.status == 'publicado':
                                print row['pk'], '...'
                                print "[02] Condominio nao enc.:", idedificio, " ->", row['fields'][u'edificio'], row['fields'][u'nomecondominio']
                                erro = True
                                break

                novo_imovel.condominio = condominio
                novo_imovel.eh_comercial = False

                tipo = int(row['fields'][u'tipo'])
                subtipo = int(row['fields'][u'idsubtipo'])
                areaurbana = row['fields'][u'areaurbana']

                if tipo == 1 or subtipo == 8:
                    novo_imovel.tipo_imovel = "casa"
                elif tipo == 2:
                    novo_imovel.tipo_imovel = "apartamento"
                elif tipo == 3:
                    novo_imovel.tipo_imovel = "terreno"
                elif tipo == 4:
                    novo_imovel.eh_comercial = True
                    if subtipo == 9:
                        novo_imovel.tipo_imovel = "galpao"
                    elif subtipo == 10:
                        novo_imovel.tipo_imovel = "terreno"
                    elif subtipo == 18:
                        novo_imovel.tipo_imovel = "edificio"
                    elif subtipo == 19:
                        novo_imovel.tipo_imovel = "loja"
                    elif subtipo == 21:
                        novo_imovel.tipo_imovel = "casa"
                        novo_imovel.eh_casa_sobrado = True
                    elif subtipo == 22:
                        novo_imovel.tipo_imovel = "sala"
                    elif subtipo == 33:
                        novo_imovel.tipo_imovel = "chacara"
                    elif subtipo == 36:
                        novo_imovel.tipo_imovel = "sala"
                elif tipo == 6 or areaurbana == 'S':
                    novo_imovel.tipo_imovel = "areaurbana"
                elif tipo == 12:
                    novo_imovel.tipo_imovel = "chacara"

                # subtipos para casa
                if subtipo == 29:
                    novo_imovel.eh_casa_terrea = True
                elif subtipo == 30:
                    novo_imovel.eh_casa_sobrado = True
                elif subtipo == 31:
                    novo_imovel.eh_casa_edicula = True
                elif subtipo == 32:
                    novo_imovel.eh_casa_sobreloja = True

                # subtipos para apartamento
                if subtipo in [14, 15, 16]:
                    novo_imovel.eh_apto_cobertura = True

                if subtipo == 15 or subtipo == 17:
                    novo_imovel.eh_apto_duplex = True
                elif subtipo == 16:
                    novo_imovel.eh_apto_triplex = True

                novo_imovel.esta_ocupado = False
                if row['fields'][u'situacao'] == 'O':
                    novo_imovel.esta_ocupado = True

                novo_imovel.esta_mobiliado = False
                if row['fields'][u'mobiliado'] == 'S':
                    novo_imovel.esta_mobiliado = True

                tipotransacao = "venda"
                if int(row['fields'][u'finalidade']) == 2:
                    tipo_transacao = "locacao"

                idbairro = row['fields'][u'idbairro']
                try:
                    bairro = Bairro.objects.get(pk=idbairro)
                except:
                    bairro = None

                if not bairro and novo_imovel.status == 'publicado':
                    print row['pk'], '...'
                    print "[03] Bairro invalido: ", row['fields'][u'idbairro'], " >", row['fields'][u'bairro'], "< ", row['fields'][u'cidade']
                    if bairro:                        
                        print "[03] Bairro invalido: ", bairro.id, " >", bairro.nome, "<"
                    erro = True
                    break
                elif row['fields'][u'bairro'] and not bairro.nome == row['fields'][u'bairro'].title():
                    if novo_imovel.status == 'publicado':
                        bairro_validar_count += 1
                        # print row['pk'], '...'
                        # print "    ---> [03] Validar o Bairro invalido: ",
                        # row['fields'][u'idbairro'], " >",
                        # row['fields'][u'bairro'], "< ", row['fields'][u'cidade']

                novo_imovel.cep = row['fields'][u'cep']
                novo_imovel.logradouro = row['fields'][u'logradouro']
                novo_imovel.numero = row['fields'][u'numero']
                novo_imovel.complemento = row['fields'][u'complemento']
                # row['fields'][u'complemente']
                if bairro:
                    novo_imovel.bairro = bairro
                    novo_imovel.regiao = bairro.regiao
                    novo_imovel.cidade = bairro.cidade

                if novo_imovel.condominio:
                    condominio_updated = False
                    if not novo_imovel.condominio.cep:
                        condominio_updated = True
                        novo_imovel.condominio.cep = novo_imovel.cep

                    if not novo_imovel.condominio.logradouro:
                        condominio_updated = True
                        novo_imovel.condominio.logradouro = novo_imovel.logradouro
                        novo_imovel.condominio.numero = novo_imovel.numero
                    try:
                        sem_bairro = not novo_imovel.condominio.bairro
                    except:
                        sem_bairro = True
                    if bairro and sem_bairro:
                        condominio_updated = True
                        novo_imovel.condominio.bairro = bairro
                        novo_imovel.condominio.regiao = bairro.regiao
                        novo_imovel.condominio.cidade = bairro.cidade

                    if condominio_updated:
                        condominio_update_count += 1
                        novo_imovel.condominio.save()

                #TODO: adicionar na obs_interna
                #novo_imovel.dormitorios = row['fields'][u'area_util']
                novo_imovel.dormitorios = trata_int(row['fields'][u'dormitorios'])
                novo_imovel.area_construida = trata_int(row['fields'][u'area_construida'])
                novo_imovel.area_terreno = trata_int(row['fields'][u'area_terreno'])
                novo_imovel.banheiros = trata_int(row['fields'][u'banheiros'])
                novo_imovel.suites = trata_int(row['fields'][u'suites'])
                novo_imovel.vagas_garagem = trata_int(row['fields'][u'vagasgaragem'])
                novo_imovel.descricao_comodos = ""

                descImovel = row['fields'][u'descricao']
                if descImovel:
                    novo_imovel.descricao_imovel = descImovel.title()

                if row['fields'][u'placa'] == 'S':
                    novo_imovel.esta_com_placa = True

                if float(row['fields'][u'venda']) > 0:
                    novo_imovel.valor_venda = float(row['fields'][u'venda'])
                    novo_imovel.eh_para_venda = True

                if float(row['fields'][u'locacao']) > 0:
                    novo_imovel.valor_locacao = float(row['fields'][u'locacao'])
                    novo_imovel.eh_para_locacao = True

                if float(row['fields'][u'condominio']) > 0:
                    novo_imovel.valor_condominio = float(row['fields'][u'condominio'])

                ids_arealazer = row['fields'][u'idarealazer']
                if ids_arealazer:
                    ids_arealazer = ids_arealazer.replace(",", ";")
                    for id_alazer in ids_arealazer.split(';'):
                        try:
                            if not str(id_alazer).strip():
                                continue
                            arealazer = AreaDeLazer.objects.get(id=id_alazer)
                        except Exception as e:
                            print "--> Area de lazer não encontrada: '{0}':{1}".format(
                                id_alazer, ids_arealazer)
                            erro = True
                            break

                        try:
                            if novo_imovel.condominio:
                                arealazer_imovel = novo_imovel.condominio.areadelazer_condominio.get(
                                    pk=id_alazer)
                            else:
                                arealazer_imovel = novo_imovel.areadelazer_imovel.get(pk=id_alazer)
                        except:
                            arealazer_imovel = None

                        if not arealazer_imovel:
                            try:
                                if novo_imovel.condominio:
                                    novo_imovel.condominio.areadelazer_condominio.add(
                                        arealazer)
                                    areas_cond_count += 1
                                else:
                                    novo_imovel.areadelazer_imovel.add(
                                        arealazer)
                                    areas_imovel_count += 1

                            except Exception as e:
                                print "--> Erro ao adicionar area de lazer: {0}:{1}::{2}".format(
                                    arealazer, id_alazer, ids_arealazer)
                                erro = True
                                break

                if row['fields'][u'localchaves'] == 1:
                    novo_imovel.local_chave = 'imobiliaria'
                elif row['fields'][u'localchaves'] == 2:
                    novo_imovel.local_chave = 'proprietario'
                elif row['fields'][u'localchaves'] == 3:
                    novo_imovel.local_chave = 'portaria'
                else:
                    novo_imovel.local_chave = 'outro'

                if row['fields'][u'obschaves']:
                    novo_imovel.local_chave_observacao = row['fields'][u'obschaves']

                #TODO: Nao bate os itens da area de lazer
                #print "1:", row['fields'][u'arealazer']
                #print "1:", row['fields'][u'arealazer']

                #TODO: print "3:", 
                f_pgtos = row['fields'][u'formaspagamento']
                if 'FGTS' in f_pgtos:
                    try:
                        novo_imovel.forma_de_pagamentos.add(db_fgts)
                    except Exception as e:
                        print "--> Erro adic. forma pagto"
                        erro = True
                        break

                if 'FINANCIAMENTO' in f_pgtos.upper() or row['fields'][u'isfinanciamento'] == 'S':
                    try:
                        novo_imovel.forma_de_pagamentos.add(db_financiamento)
                    except Exception as e:
                        print "--> Erro adic. forma pagto"
                        erro = True
                        break

                if 'PROPOSTA' in f_pgtos.upper():
                    try:
                        novo_imovel.forma_de_pagamentos.add(db_proposta)
                    except Exception as e:
                        print "--> Erro adic. forma pagto"
                        erro = True
                        break
                imovel_menor_valor = 'VEL MENOR VALOR' in f_pgtos.upper() or 'VEL DE MENOR VALOR' in f_pgtos.upper()
                apto_menor_valor = 'ACEITA APAR' in f_pgtos.upper()
                if imovel_menor_valor or apto_menor_valor:
                    try:
                        novo_imovel.forma_de_pagamentos.add(db_imovelmenorvalor)
                    except Exception as e:
                        print "--> Erro adic. forma pagto"
                        erro = True
                        break

                novo_imovel.observacoes_internas = ""
                if row['fields'][u'obs']:
                    novo_imovel.observacoes_internas = row['fields'][u'obs']

                if row['fields'][u'dtinsere']:
                    novo_imovel.data_cadastro = datetime.strptime(
                        row['fields'][u'dtinsere'], "%Y-%m-%d").replace(tzinfo=timezone.utc)

                novo_imovel.save()
                print row['pk'], '... OK'

        if not erro:
            self.stdout.write('Created: %s\n' % created_count)
            self.stdout.write('Updated: %s\n' % updated_count)
            self.stdout.write('Proprietario added: %s\n' % proprietario_count)
            self.stdout.write('Areas lazer imovel added: %s\n' % areas_imovel_count)
            self.stdout.write('Areas lazer cond.  added: %s\n' % areas_cond_count)

            self.stdout.write('Condominio updated: %s\n' % condominio_update_count)
            self.stdout.write('Condominio validar: %s\n' % condominio_validar_count)
            self.stdout.write('Bairro validar: %s\n' % bairro_validar_count)
            self.stdout.write('done\n')

"""
('CARLOS'   11),
('CECILIA'  12),
('JORGE',   9),
('LADISMAN' 3),
('ODILON'   17),
('ROGER'    15),
('SILVIA'   6),

('ANDRESSA' 14),
('EDSON'    16),
('MARIA'    13),
('VERCI'    2);
"""

"""
    
    edificio,nomecondominio,idedificio,condominiofechado
    tipo,idsubtipo,areaurbana,finalidade,situacao,publicar,arquivado,mobiliado
    cep,logradouro,numero,complemento,idbairro,idcidade,idregiao,bairro,complemente,cidade,estado
    dormitorios,domirtorios,area_util,area_construida,area_terreno,banheiros,suites,placa,descricao,vagasgaragem
    venda,locacao,condominio,iptu
    arealazer,idarealazer,formaspagamento,isfinanciamento
    corretor,localchaves,obschaves

    id
    oportunidade

    foto
    caminhofoto
    nomefoto
    nomefotosite    
    
    obs
    idnew
    enviado
    dtinsere
    usuarioinsere
    dtaltera
    usuarioaltera
    motivoaltera

"""








