# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from floppyforms.widgets import (CheckboxInput,
                                 RadioSelect,
                                 CheckboxSelectMultiple, )


class SimNaoCheckboxInput(CheckboxInput):
    template_name = 'floppyforms/simnaocheckbox.html'


class CorretorRadioSelect(RadioSelect):
    template_name = 'floppyforms/corretorradio.html'


class BairroCheckboxSelectMultiple(CheckboxSelectMultiple):
    template_name = 'floppyforms/bairro_checkbox_select.html'


class BairroComImoveisCheckboxSelectMultiple(CheckboxSelectMultiple):
    template_name = 'floppyforms/bairro_comimoveis_checkbox_select.html'
