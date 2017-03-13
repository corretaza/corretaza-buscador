# -*- coding: UTF-8 -*-
import floppyforms.__future__ as forms
import re

class OnlyInteger(forms.Field):

    def clean(self, value):
        ''' Permitir somente numeros, mesmo os exponencias como, 10e1 '''
        if value and (re.search(u'[A-z]', value) or not(re.match(u'[0-9]', value))):
            raise forms.ValidationError("Somente Números")


class CustomInteger(OnlyInteger, forms.IntegerField):

    def __init__(self, initial=0, min_value=0, *args, **kwargs):
        kwargs.update(dict(initial=initial, min_value=min_value))
        super(CustomInteger, self).__init__(*args, **kwargs)


class MultipleInteger(OnlyInteger, forms.CharField):

    def __init__(self, *args, **kwargs):
        super(MultipleInteger, self).__init__(*args, **kwargs)

    def clean(self, values):
        super(MultipleInteger, self).clean(values)
        if values:
            for value in values.split(","):
                if value and not re.match(u'^[0-9]+$', value.strip()):
                    raise forms.ValidationError("Somente Números separados por ' , ' ")
