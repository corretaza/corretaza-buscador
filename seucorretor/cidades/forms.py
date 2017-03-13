# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

import floppyforms.__future__ as forms

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from .models import Cidade, Regiao, Bairro


class BairroForm(forms.ModelForm):

    class Meta:
        model = Bairro
        fields = ('nome', 'nome_popular',
            'cidade', 'regiao', )


class RegiaoForm(forms.ModelForm):

    class Meta:
        model = Regiao
        fields = ('nome', 'cidade' )


class CidadeForm(forms.ModelForm):

    class Meta:
        model = Cidade
        fields = ('nome', )
