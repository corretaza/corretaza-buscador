# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from sh import rm

from django.views.generic.edit import FormView
from django.views.generic import ListView, TemplateView
from django.contrib.sites.models import Site
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from django.core.management import call_command
from django.http import HttpResponse

from StringIO import StringIO
from braces.views import LoginRequiredMixin, UserPassesTestMixin

from .models import PropertyList, ImovelVivaReal
from .forms import VivaRealUploadFileForm

from django.shortcuts import render
from datetime import datetime


class VivaRealFileUploadFormView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    form_class = VivaRealUploadFileForm
    template_name = "vivareal/vivareal_upload_xml.html"

    def test_func(self, user):
        return user.is_authenticated() and user.userprofile.is_admin

    def get_success_url(self):
        return reverse('vivareal.upload.completo')

    def form_valid(self, form):
        target_filename = 'vivarealfile.xml'
        vivarealfile = self.get_form_kwargs().get('files')['vivarealfile']

        fileuploaded = default_storage.save(target_filename,
                                            ContentFile(vivarealfile.read()))

        fileuploaded = settings.MEDIA_ROOT + '/%s' % fileuploaded

        results = StringIO()
        call_command('importar_imoveis', file=fileuploaded, stdout=results)

        try:
            rm(fileuploaded)
        except:
            pass

        return super(VivaRealFileUploadFormView, self).form_valid(form)


class VivaRealUploadCompletoListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = PropertyList
    paginate_by = '100'
    context_object_name = 'property_list'
    template_name = "vivareal/uploads.html"

    def test_func(self, user):
        return user.is_authenticated() and user.userprofile.is_admin

    def get_context_data(self, **kwargs):
        context = super(VivaRealUploadCompletoListView, self) \
                      .get_context_data(**kwargs)

        context['imoveis_disponiveis'] = PropertyList.objects.filter(
            archived=False, new=False).count()
        context['imoveis_novos'] = PropertyList.objects.filter(
            new=True).count()
        context['imoveis_arquivados'] = PropertyList.objects.filter(
            archived=True).count()

        return context

    def get_queryset(self):
        return PropertyList.objects.all()


class VivaRealXML(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    content_type = "application/xml"
    # content_type = "text/plain"
    template_name = "vivareal/xml_base.xml"
    arquivo_xml_query = None

    def test_func(self, user):
        return user.is_authenticated() and (user.userprofile.is_admin)

    def get_context_data(self, **kwargs):
        context = super(VivaRealXML, self).get_context_data(**kwargs)
        context['data'] = datetime.today()
        #context['imoveis'] = ImovelVivaReal.objects_geral.publicados().order_by('-id')
        # TODO: Passar isto para o manager!
        self.arquivo_xml_query = ImovelVivaReal.objects_geral.publicados().exportar_para_portais().order_by(
            '-atualizado_em').select_related(
            'cidade', 'bairro', 'regiao', 'foto_principal', 'foto' )
        context['imoveis'] = self.arquivo_xml_query
        context['domain'] = Site.objects.get_current()
        return context

    def render_to_response(self, context, **response_kwargs):
        xml = super(VivaRealXML, self).render_to_response(context, **response_kwargs)
        response = HttpResponse(xml.rendered_content, content_type='application/xml')
        filename = "imoveis_para_vivareal_{}.xml".format(datetime.today())
        #filename = "imoveis_vivareal_201608121558.xml" #BUGFIX resolvido, nao precisa ser nomefixo
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        return response
