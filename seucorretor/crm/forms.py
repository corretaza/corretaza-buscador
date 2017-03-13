# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

import floppyforms.__future__ as forms

from floppyforms.widgets import (TextInput, )
from django.db.models import Q

from imobiliaria.validators import phone_validator

from .models import Proprietario


def verifica_fone(fone, instance):
    """ validate and remove spaces from phone numbers """
    if not fone:
        return fone
    fone_existente = Proprietario.objects.filter(
        Q(fone__contains=fone) |
        Q(fone2__contains=fone) |
        Q(fone3__contains=fone) |
        Q(fone4__contains=fone))

    if instance and fone_existente and fone_existente[0].id == instance.id:
        return fone

    if fone_existente:
        raise forms.ValidationError(
            "{0} já cadastrado para {1}".format(fone, fone_existente[0]))
    return fone


class ProprietarioForm(forms.ModelForm):

    class Meta:
        model = Proprietario
        fields = ('nome', 'nome_conjuge',
                  'fone', 'fone_melhorhora', 'fone2', 'fone2_melhorhora',
                  'fone3', 'fone3_melhorhora',
                  'fone4', 'whatsapp',
                  'email', 'email_alternativo', 'melhor_forma_contato',
                  'observacoes', )
        widgets = {
            'fone_melhorhora': TextInput(),
            'fone2_melhorhora': TextInput(),
            'fone3_melhorhora': TextInput(),
        }

    def clean_fone(self):
        fone_validated = phone_validator(self.cleaned_data.get('fone'))
        self.cleaned_data['fone'] = verifica_fone(fone_validated, self.instance)
        return self.cleaned_data['fone']

    def clean_fone2(self):
        fone_validated = phone_validator(self.cleaned_data.get('fone2'))
        self.cleaned_data['fone2'] = verifica_fone(fone_validated, self.instance)
        return self.cleaned_data['fone2']

    def clean_fone3(self):
        fone_validated = phone_validator(self.cleaned_data.get('fone3'))
        self.cleaned_data['fone3'] = verifica_fone(fone_validated, self.instance)
        return self.cleaned_data['fone3']

    def clean_fone4(self):
        fone_validated = phone_validator(self.cleaned_data.get('fone4'))
        self.cleaned_data['fone4'] = verifica_fone(fone_validated, self.instance)
        return self.cleaned_data['fone4']
