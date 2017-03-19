# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

import floppyforms.__future__ as forms

from floppyforms.widgets import (HiddenInput,
                                 CheckboxSelectMultiple, )
from image_cropping import ImageCropWidget

from ibuscador.models import Imovel, Foto, Condominio
from cidades.models import Bairro, Regiao


class NovoImovelPasso1Form(forms.ModelForm):

    class Meta:
        model = Imovel
        fields = ('proprietario', )


class NovoImovelPasso1ConfirmacaoForm(forms.ModelForm):

    class Meta:
        model = Imovel
        fields = ('eh_comercial',
                  'tipo_imovel',
                  'valor_venda',
                  'cidade',
                  'proprietario', )

    def __init__(self, *args, **kwargs):
        super(NovoImovelPasso1ConfirmacaoForm,
              self).__init__(*args, **kwargs)
        self.fields['valor_venda'].label = 'Valor'
        self.fields['cidade'].required = True

    def clean_valor_venda(self):
        valor_venda = self.cleaned_data.get('valor_venda')
        if int(valor_venda) <= 0:
            raise forms.ValidationError('Valor inválido')
        return self.cleaned_data['valor_venda']

    def clean_tipo_imovel(self):
        if self.cleaned_data.get('eh_comercial') and self.cleaned_data.get('tipo_imovel') == 'apartamento':
            raise forms.ValidationError('Apartamento não pode ser comercial.')
        return self.cleaned_data.get('tipo_imovel')


class NovoImovelPasso2Form(forms.ModelForm):

    class Meta:
        model = Imovel
        fields = ('condominio',)

    def __init__(self, cidade=None, *args, **kwargs):
        super(NovoImovelPasso2Form, self).__init__(*args, **kwargs)
        self.fields["condominio"].queryset = Condominio.objects.filter(cidade__nome=cidade)


class NovoImovelPasso3Form(forms.ModelForm):

    class Meta:
        model = Imovel
        fields = ('valor_condominio', 'cep', 'logradouro', 'numero',
                  'complemento', 'bairro', 'regiao', 'cidade', )

    def __init__(self, cidade=None, *args, **kwargs):
        super(NovoImovelPasso3Form, self).__init__(*args, **kwargs)
        self.fields['bairro'].queryset = Bairro.objects.filter(cidade__nome=cidade).\
            order_by('nome')
        self.fields['regiao'].queryset = Regiao.objects.filter(cidade__nome=cidade).\
            order_by('nome')


class ImovelForm(forms.ModelForm):

    class Meta:
        model = Imovel
        fields = (
                  'eh_apto_duplex',
                  'eh_apto_triplex',
                  'eh_apto_cobertura',
                  'eh_casa_terrea',
                  'eh_casa_edicula',
                  'eh_casa_sobreloja',
                  'eh_casa_sobrado',
                  'eh_casa_geminada',
                  'eh_kitnet',
                  'eh_imovel_novo',
                  'eh_comercial',
                  'imovel_ref',
                  'eh_para_locacao',
                  'valor_locacao',
                  'eh_para_venda',
                  'valor_venda',
                  'valor_condominio',
                  'dormitorios',
                  'banheiros',
                  'suites',
                  'vagas_garagem',
                  'area_construida',
                  'area_terreno',
                  'dimensoes_terreno',
                  'descricao_imovel',
                  'descricao_comodos',
                  'esta_ocupado',
                  'esta_mobiliado',
                  'esta_com_placa',
                  'local_chave',
                  'local_chave_observacao',
                  'observacoes_internas',
                  'forma_de_pagamentos',
                  'outra_forma_de_pagamento',
                  'areadelazer_imovel',
                  'cep', 'cidade', 'logradouro',
                  'numero', 'complemento',
                  'bairro', 'regiao',
                  'condominio',
                  'proprietario',
                  'corretores',
                  'indicado_por',
                  'nao_exportar_para_portais',
                  'tipo_varanda', )
        widgets = {
            'imovel_ref': HiddenInput(),
            'areadelazer_imovel': CheckboxSelectMultiple(attrs={'size': 16, }),
            'corretores': CheckboxSelectMultiple(attrs={'size': 16, }),
            'forma_de_pagamentos': CheckboxSelectMultiple(attrs={'size': 8, }),
        }

    def __init__(self, cidade=None, *args, **kwargs):
        super(ImovelForm, self).__init__(*args, **kwargs)
        self.fields['bairro'].queryset = Bairro.objects.filter(cidade__nome=cidade).\
            order_by('nome')
        self.fields['regiao'].queryset = Regiao.objects.filter(cidade__nome=cidade).\
            order_by('nome')
        self.fields['condominio'].queryset = Condominio.objects.filter(cidade__nome=cidade).\
            order_by('nome')


class ImovelTipoForm(forms.ModelForm):

    class Meta:
        model = Imovel
        fields = ('tipo_imovel', )


class ImovelFotoUploadForm(forms.ModelForm):

    class Meta:
        model = Foto
        exclude = ('imovel', )


class ImovelFotoForm(forms.ModelForm):

    class Meta:
        model = Foto
        fields = ('descricao',
                  'ordem',
                  'eh_principal',
                  'picture_cropping', 'picture' )
        widgets = {
            'picture': ImageCropWidget,
        }


class ImovelPublicarForm(forms.ModelForm):

    class Meta:
        model = Imovel
        fields = ('status', )
        widgets = {
            'status': HiddenInput(),
        }