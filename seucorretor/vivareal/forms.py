# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

import floppyforms.__future__ as forms


class VivaRealUploadFileForm(forms.Form):

    """
    Override the default authentication
    """
    vivarealfile = forms.FileField(label='Select a vivareal file')
