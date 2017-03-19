# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

import floppyforms.__future__ as forms

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models import F

from floppyforms.widgets import (HiddenInput,
                                 Textarea,
                                 RadioSelect,
                                 CheckboxSelectMultiple, )

from model_utils import Choices

from magicemailtemplates.sender import MagicEmail

from cidades.models import Cidade
from themes.widgets import BairroComImoveisCheckboxSelectMultiple
from imobiliaria import preferences

from .form import CustomInteger, MultipleInteger
from .models import BairroComImoveis, Condominio, Imovel, HistoricoDeImovel
from .models import InteresseBase


class BuscaInicialForm(forms.Form):

    tipo_interesse = forms.CharField()
    tipo_imovel = forms.CharField()
    cidade = forms.CharField()
    imovel_ref = forms.CharField(required=False)
    residencial_comercial = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(BuscaInicialForm, self).__init__(*args, **kwargs)
        self.fields['tipo_interesse'] = forms.ChoiceField(
            choices=InteresseBase.TIPOS_INTERESSE)
        self.fields['tipo_interesse'].label = "Interesse"
        self.fields['tipo_imovel'] = forms.ChoiceField(
            choices=tuple(Imovel.TIPO_IMOVEL))
        self.fields['tipo_imovel'].label = "Tipo do imóvel"
        cidade_list = [(cidade.nome, cidade.nome) for cidade in Cidade.objects.all()]
        self.fields['cidade'] = forms.ChoiceField(
            choices=cidade_list)
        opcoes_list = (('residencial', 'Residencial'),
                       ('comercial', 'Comercial'), )
        self.fields['residencial_comercial'] = forms.ChoiceField(
            label='',
            choices=tuple(opcoes_list),
            initial='residencial',
            widget=RadioSelect())


class FiltroPorValorForm(forms.Form):
    CHOICES_EM_CONDOMINIO = ((True, "Apenas em condomínio fechado"),
                          ("", "Indiferente"))
    CHOICES_MOBILIADO = (("mobiliado", "Mobiliado"),
                         ("nao_mobiliado", "Não Mobiliado"),
                         ("", "Indiferente"))
    CHOICES_STATUS = (("publicado", "Publicado"),
                      ("arquivado", "Arquivado"))
    valor_min = CustomInteger()
    valor_max = CustomInteger()
    min_quarto = CustomInteger()
    min_vaga = CustomInteger()
    area_min = CustomInteger()
    codigo_referencia = MultipleInteger(label="Código Referência", required=False)
    bairros = forms.MultipleChoiceField(required=False)
    em_condominio = forms.ChoiceField(choices=CHOICES_EM_CONDOMINIO,
                                   widget=forms.RadioSelect(),
                                   initial=CHOICES_EM_CONDOMINIO[-1],
                                   label="Condomínio Fechado?",
                                   required=False)
    mobiliado = forms.ChoiceField(choices=CHOICES_MOBILIADO,
                                   widget=forms.RadioSelect(),
                                   initial=CHOICES_MOBILIADO[-1],
                                   label="Mobília",
                                   required=False)
    status = forms.ChoiceField(choices=CHOICES_STATUS,
                                   widget=forms.RadioSelect(),
                                   initial=CHOICES_STATUS[0],
                                   label="Status",
                                   required=False)
    condominio = forms.ChoiceField(widget=forms.Select(),
                                        label="Condomínio",
                                        required=False)

    def __init__(self, tipo_imovel=None, tipo_interesse=None, cidade=None, *args, **kwargs):
        super(FiltroPorValorForm, self).__init__(*args, **kwargs)
        qs = BairroComImoveis.objects.filter(
            tipo_imovel=tipo_imovel, cidade__nome=cidade).select_related('cidade', 'bairro' )
        if tipo_interesse == 'comprar':
            qs = qs.filter(contador_venda__gt=0)
        else:
            qs = qs.filter(contador_locacao__gt=0)

        bairro_list = [(bairro.bairro.id, bairro) for bairro in qs]
        bairro_list = sorted(bairro_list, key = lambda tup: tup[1].bairro.descricao)

        condominio_list = [('', '---------------')]
        condominio_list += [(condominio.id, condominio.nome)
                           for condominio in Condominio.objects.filter(cidade__nome=cidade).select_related('cidade', )]
        self.fields['bairros'].widget = BairroComImoveisCheckboxSelectMultiple(
          attrs={'tipo_interesse': tipo_interesse})
        self.fields["condominio"].choices = condominio_list
        self.fields["condominio"].initial = condominio_list[0]
        self.fields['bairros'].choices = bairro_list


class NovoCondominioForm(forms.ModelForm):

    class Meta:
        model = Condominio
        fields = ('nome',
                  'cep', 'cidade', 'logradouro', 'numero',
                  'bairro', 'regiao',
                  'blocos', 'andares',
                  'apto_por_andar',
                  'tem_elevador',
                  'construtora', 'ano_construcao',
                  'contato_portaria',
                  'contato_zelador',
                  'contato_administradora',
                  'regras_mudanca',
                  'areadelazer_condominio',
                  'portaria', )
        widgets = {
            'areadelazer_condominio': CheckboxSelectMultiple(attrs={'size': 16, }),
        }


class ContatarAnuncianteForm(forms.Form):
    CONTATOS_VIA = Choices(('email', _('Email')),
                           ('fone', _('Fone')),
                           ('whatsapp', _('WhatsApp')), )
    imovel_ref = forms.CharField(widget=forms.HiddenInput())
    email = forms.EmailField(
      widget=forms.TextInput(attrs={'placeholder': 'Digite seu email'}))
    telefone = forms.CharField(
      widget=forms.TextInput(attrs={'placeholder': 'Digite seu telefone'}))
    nome = forms.CharField(
      widget=forms.TextInput(attrs={'placeholder': 'Digite seu nome e sobrenome'}),
      label='Nome e Sobrenome')
    mensagem = forms.CharField(
      widget=forms.Textarea(attrs={'rows': 3,
                                   'cols': 35,
                                   'placeholder': 'Opcionalmente, você pode deixar uma mensagem'}),
      required=False)
    receber_contato = forms.CharField(
      label='Desejo receber contato por',
      widget=forms.CheckboxSelectMultiple(choices=CONTATOS_VIA),
      required=False)

    def __init__(self, *args, **kwargs):
        super(ContatarAnuncianteForm, self).__init__(*args, **kwargs)

    def clean_telefone(self):
        telefone = self.cleaned_data['telefone']
        # not re.match(r'^(\(\d{2}\)) ?(\d{5}-\d{4}|\d{9}|\d{4}-\d{4}|\d{8})$',
        # telefone)
        if len(telefone) < 9:
            raise forms.ValidationError("Digite um telefone válido.")
        return telefone

    def envia_email(self):
        sender = MagicEmail("{0}".format(settings.DEFAULT_FROM_EMAIL))
        current_site = Site.objects.get_current()
        subject = "[SJC Vale Imóveis] Novo Contato: Ref: {0} ".format(
          self.cleaned_data['imovel_ref'])
        data = {'domain': current_site.domain,
                'body': subject,
                'imovel_ref': self.cleaned_data['imovel_ref'],
                'email': self.cleaned_data['email'],
                'telefone': self.cleaned_data['telefone'],
                'nome': self.cleaned_data['nome'],
                'mensagem': self.cleaned_data['mensagem'],
                'receber_contato': self.cleaned_data['receber_contato'],
                'url': reverse('buscador.lista.imovel_referencia',
                               args=[self.cleaned_data['imovel_ref'], ]), }

        email_contato = preferences.ImobiliariaPreferences.email_contato
        sender.using_template(
            "contato_cliente_imovel", data) \
            .with_subject(subject) \
            .reply_to(self.cleaned_data['email']) \
            .send_to([email_contato, ])


class HistoricoDeImovelForm(forms.ModelForm):

    class Meta:
        model = HistoricoDeImovel
        fields = ('conteudo', )
        widgets = {
            'conteudo': Textarea(attrs={'rows': 4, 'cols': 35}),
        }
