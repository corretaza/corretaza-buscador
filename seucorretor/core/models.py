# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

#from djrill.signals import webhook_event

"""
@receiver(webhook_event)
def handle_inbound(sender, event_type, data, **kwargs):
    '''
       Intercepta todos os emails recebidos (inbound) os quais se enquadram
       na classificação registrada no backend de email (e.g. mandrill)
    '''
    if event_type == 'inbound':

        email = data['msg']['from_email']
        subject = data['msg']['subject']
        html = data['msg']['html']

        engine.EmailInboundProcessor.with_email(
            html).from_email(email).subject(subject).process()
"""
