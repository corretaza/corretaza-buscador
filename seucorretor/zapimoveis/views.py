# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from datetime import datetime

from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.contrib.sites.models import Site
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from braces.views import LoginRequiredMixin, UserPassesTestMixin

from imobiliaria import preferences
from .models import ImovelZapImovel, ImovelWeb



class ZapImoveisXML(TemplateView):
    content_type = "application/xml"
    template_name = "zapimoveis/xml_base.xml"

    def get_context_data(self, **kwargs):
        context = super(ZapImoveisXML, self).get_context_data(**kwargs)
        context['data'] = datetime.today()
        # TODO: Passar isto para o manager!
        arquivo_xml_query = ImovelZapImovel.objects_geral.publicados().order_by('-id').select_related(
            'cidade', 'bairro', 'regiao', 'foto_principal', 'foto' )

        limite = preferences.ZapPreferences.qtd_imoveis_para_exportacao
        context['imoveis'] = arquivo_xml_query[:limite]
        context['domain'] = Site.objects.get_current()
        return context

    def render_to_response(self, context, **response_kwargs):
        xml = super(ZapImoveisXML, self).render_to_response(context, **response_kwargs)
        response = HttpResponse(xml.rendered_content, content_type='application/xml')
        #filename = "imoveis_para_zapimoveis_{}.xml".format(datetime.today())
        #response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        return response


class ImovelWebXML(TemplateView):
    content_type = "application/xml"
    template_name = "zapimoveis/xml_imovelweb.xml"

    def get_context_data(self, **kwargs):
        context = super(ImovelWebXML, self).get_context_data(**kwargs)
        context['data'] = datetime.today()
        # TODO: Passar isto para o manager!
        arquivo_xml_query = ImovelWeb.objects_geral.publicados().order_by('-id').select_related(
            'cidade', 'bairro', 'regiao', 'foto_principal', 'foto' )
        context['imoveis'] = arquivo_xml_query
        context['domain'] = Site.objects.get_current()
        return context

    def render_to_response(self, context, **response_kwargs):
        xml = super(ImovelWebXML, self).render_to_response(context, **response_kwargs)
        response = HttpResponse(xml.rendered_content, content_type='application/xml')
        return response
