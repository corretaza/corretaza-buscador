# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from braces.views import LoginRequiredMixin, UserPassesTestMixin
from rolepermissions.verifications import has_role

from seucorretor.roles import Gerente, Corretor


class EhGerenteMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self, user):
        return has_role(user, [Gerente, ])


class EhCorretorMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self, user):
        return has_role(user, [Gerente, Corretor, ])
