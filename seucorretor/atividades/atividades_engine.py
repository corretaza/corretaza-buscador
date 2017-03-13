# -*- coding: utf-8 -*-

from django.utils import timezone

from .models import Atividade


class Atividades(object):

    """
     Ator  Ação     Objeto    Detalhes
     /     /        /         /
    Jose registrou contato [...] 12 horas atrás

    Uso:
    Atividades.do('Jose').que('Registrou').um('Contato','[...]').no(Interesse.id)

    """
    @classmethod
    def do(cls, ator):
        return cls(ator)

    def __init__(self, ator):
        self.ator = ator
        self.acao = None
        self.objeto = None
        self.detalhe = None
        self.data = None
        self.interesse = None

    def que(self, acao):
        self.acao = acao
        return self

    def um(self, objeto, detalhe=''):
        self.objeto = objeto
        self.detalhe = detalhe
        return self

    def no(self, interesse):
        self.interesse = interesse
        return self

    def registrar(self):
        ''' cria novo registro de atividade '''
        Atividade.objects.create(
            ator=self.ator, acao=self.acao, objeto=self.objeto,
            detalhe=self.detalhe, interesse=self.interesse)
        return self

    def atualizar(self):
        ''' atualiza ultima atividade criada '''
        atividade, created = Atividade.objects.get_or_create(
            ator=self.ator, acao=self.acao, objeto=self.objeto,
            interesse=self.interesse)
        agora = timezone.now()
        atividade.detalhe += '\n------> {0}:\n{1}'.format(
            agora.strftime("%d %b %Y %H:%M"), self.detalhe)
        atividade.data = agora
        atividade.save()
        return self

    def listar_todas(self):
        return Atividade.objects.filter(interesse=self.ator)
