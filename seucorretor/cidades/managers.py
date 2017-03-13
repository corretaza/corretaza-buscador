from django.db import models


class Queryset(models.query.QuerySet):

    def por_cidade(self, cidade):
        return self.filter(cidade__nome=cidade)


class ManagerBase(models.Manager):

    def get_queryset(self):
        return Queryset(self.model, using=self._db)

    def por_cidade(self, cidade):
        return self.get_queryset().por_cidade(cidade)
