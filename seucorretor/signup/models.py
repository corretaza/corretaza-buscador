# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

import logging

from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from django.db import models
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in

from rolepermissions.shortcuts import retrieve_role

from seucorretor.roles import (
    Gerente, Corretor, Estagiario, )

from registration.signals import user_registered, user_activated
from imobiliaria.models import Colaborador

logger = logging.getLogger(__name__)


@receiver(user_activated)
def login_on_activation(sender, user, request, **kwargs):
    """Logs in the user after activation"""
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)


@receiver(user_logged_in)
def sig_user_logged_in(sender, user, request, **kwargs):
    if not UserProfile.objects.filter(user=user):
        UserProfile.objects.create(user=user)
        logger.info(
            "---> É necessário configurar um perfil para este usuário.")


class UserProfile(models.Model):

    """ Extra User information """
    ACCOUNT_GERENTE = u'gerente'
    ACCOUNT_CORRETOR = u'corretor'
    ACCOUNT_ESTAGIARIO = u'estagiario'

    ACCOUNT_TYPE = ((ACCOUNT_GERENTE, u'Gerente'),
                    (ACCOUNT_CORRETOR, u'Corretor'),
                    (ACCOUNT_ESTAGIARIO, u'Estagiario'),
                    )
    user = models.OneToOneField(User)
    account_type = models.CharField(
        max_length=32, choices=ACCOUNT_TYPE,
        default=ACCOUNT_ESTAGIARIO, blank=True)
    corretor = models.ForeignKey(
        Colaborador, verbose_name=_('corretor'),
        null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Users Profile'

    def save(self, *args, **kwargs):
        if self.account_type:
            role = retrieve_role(self.account_type)
            role.assign_role_to_user(self.user)
        super(UserProfile, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.user.first_name or self.user.username

    @property
    def is_corretor(self):
        return self.account_type == UserProfile.ACCOUNT_CORRETOR

    @property
    def has_corretor(self):
        return self.corretor or False

    def is_the_corretor(self, corretor):
        # TODO: usar django-role-perssions ao inves disto
        return self.account_type == UserProfile.ACCOUNT_CORRETOR and \
            self.corretor.id == corretor.id

    @property
    def is_admin(self):
        # TODO: remover este metodo...(roles)
        return self.account_type == UserProfile.ACCOUNT_GERENTE


@receiver(user_registered)
def create_user_profile(sender, user, request, **kwargs):
    """ Create a user profile for every new user created """
    UserProfile.objects.create(user=user, account_type='')
