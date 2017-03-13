# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

import floppyforms.__future__ as forms
from floppyforms.widgets import Textarea

from .models import Atividade


class AtividadeForm(forms.ModelForm):

    class Meta:
        model = Atividade
        fields = ('detalhe',)
        widgets = {
            'detalhe': Textarea(attrs={'rows': 6, 'cols': 35}),
        }
