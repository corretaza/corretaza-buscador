# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.db import models
from django.db.models import Q


class AtendimentoQueryset(models.query.QuerySet):

    def por_fone(self, fone):
        qs = self.filter(
            Q(fone__contains=fone) |
            Q(fone2__contains=fone) |
            Q(fone3__contains=fone) |
            Q(fone4__contains=fone))
        return qs

    def por_palavras(self, palavras):
        qs = self.filter(
            Q(fone__contains=palavras) |
            Q(fone2__contains=palavras) |
            Q(fone3__contains=palavras) |
            Q(fone4__contains=palavras) |
            Q(nome__icontains=palavras) |
            Q(email__icontains=palavras))
        return qs.order_by('-id')

    def por_email(self, email):
        qs = self.filter(email__icontains=email)
        return qs


class AtendimentoManager(models.Manager):

    def get_queryset(self):
        return AtendimentoQueryset(self.model, using=self._db)

    def por_fone(self, fone):
        return self.get_queryset().por_fone(fone)

    def por_palavras(self, palavras):
        return self.get_queryset().por_palavras(palavras)

    def por_email(self, email):
        return self.get_queryset().por_email(email)
