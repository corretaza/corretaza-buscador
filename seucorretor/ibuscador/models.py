# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from unicodedata import normalize

from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.exceptions import ObjectDoesNotExist
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User

from image_cropping import ImageRatioField

from model_utils import Choices
from crm.models import Proprietario
from cidades.models import ComEndereco, Bairro, Regiao, Cidade
from imobiliaria.models import Corretor

from .managers import (ImovelVendasManager,
                       ImovelLocacoesManager,
                       ImovelManagerBase, )
from cidades.managers import ManagerBase


class InteresseBase(models.Model):
    TIPOS_INTERESSE = (
        ('comprar', 'Comprar'),
        ('alugar', 'Alugar'),
    )
    TIPOS_URGENCIA = (
        ('0', 'Muito urgente'),
        ('1', 'Urgente'),
        ('2', 'Não urgente'),
        ('9', ' --- '),
    )
    TIPOS_IMOVEL = (
        ('apartamento', 'Apartamento'),
        ('casa', 'Casa'),
        ('terreno', 'Terreno'),
        ('areaurbana', 'Área urbana'),
        ('chacara', 'Chácara/Sítio'),
        ('loja', 'Loja/Ponto'),
        ('sala', 'Sala/Consultório'),
        ('galpao', 'Galpão/Depósito'),
        ('edificio', 'Edifício/Prédio'),
    )
    CRIADO_VIA_LIST = (
        ('vivareal', 'VivaReal'),
        ('zap', 'Zap'),
        ('imovelweb', 'Imovel Web'),
        ('placa', 'Placa'),
        ('indicacao', 'Indicação'),
        ('site', 'Site'),
        ('fone', 'Fone'),
        ('email', 'Email'),
        ('outros', 'Outros'),
    )
    TIPOS_FINALIZACAO = (
        ('sucesso', 'Imóvel vendido/alugado com sucesso!'),
        ('nao_retorna', 'Cliente não retorna contato ou sem interesse'),
        ('desistiu', 'Desistiu do imóvel ou vai dar um tempo'),
        ('sem_imovel', 'Não foi possível localizar imóvel para o perfil'),
        ('negociando_outro', 'Já achou ou esta negociando com outra imobiliaria'),
        ('engano', 'Atendimento foi cadastrado por engano'),
        ('outro', 'Outro'),
    )
    TIPOS_CANCELAMENTO = (
        ('fechou_neg', 'Já achei um imóvel'),
        ('poucasopcoes', 'Não recebi opções de imóveis do meu interesse'),
        ('atend_ruim', 'Atendimento ruim ou muito demorado'),
        ('muito_email', 'Muitos emails que não tenho interesse'),
        ('corretor', 'Não gostei do corretor'),
        ('engano', 'Me cadastrei por engano e não quero um imóvel'),
        ('outro', 'Outro'),
        ('nao_cancelar', 'Quero continuar o atendimento e receber mais opções de imóveis!'),
    )

    class Meta:
        abstract = True

    def __str__(self):
        return "ToBeExtended"


@python_2_unicode_compatible
class FormaDePagamento(models.Model):
    descricao = models.CharField(
        _('Forma de pagamento'), max_length=64, unique=True)

    class Meta:
        verbose_name = _("Forma de Pagamento")
        verbose_name_plural = _("Formas de Pagamento")
        ordering = ('descricao', )

    def __str__(self):
        return self.descricao


@python_2_unicode_compatible
class AreaDeLazer(models.Model):
    descricao = models.CharField(
        _('Área de lazer'), max_length=128, unique=True)
    tag_vivareal = models.CharField(
        _('Tag vivareal'), max_length=64, blank=True, default='')

    class Meta:
        verbose_name = _("Área de lazer")
        verbose_name_plural = _("Áreas de lazer")
        ordering = ('descricao', )

    def __str__(self):
        return self.descricao


@python_2_unicode_compatible
class Condominio(ComEndereco):
    TIPO_PORTARIA = Choices(('', _('-')),
                            ('semportaria', _('Sem Portaria')),
                            ('semporteiro', _('Sem Porteiro')),
                            ('24h', _('Portaria 24h')),
                            ('eletronica', _('Eletrônica')),
                            ('hcomercial', _('Em Horário Comercial')),
                            ('cameras', _('Com Cameras')), )

    data_cadastro = models.DateTimeField(_('data cadastro'), auto_now_add=True)
    atualizado_em = models.DateTimeField(_('atualizado em'), auto_now=True)
    nome = models.CharField(
        _('Nome do condomínio'), max_length=128, unique=True)
    blocos = models.PositiveSmallIntegerField(
        _('Qtd de blocos'), blank=True, default=0)
    andares = models.PositiveSmallIntegerField(
        _('Número de andares'), blank=True, default=0)
    apto_por_andar = models.PositiveSmallIntegerField(
        _('Apto por andar'), blank=True, default=0)
    tem_elevador = models.BooleanField(_('Tem elevador'), default=False)
    construtora = models.CharField(
        _('Nome da construtora'), max_length=256, blank=True)
    ano_construcao = models.PositiveIntegerField(
        _('Ano construção'), blank=True, default=0)
    areadelazer_condominio = models.ManyToManyField(AreaDeLazer, blank=True)
    contato_portaria = models.CharField(
        _('Contato portaria'), blank=True, max_length=128, default='')
    contato_zelador = models.CharField(
        _('Contato zelador'), blank=True, max_length=128, default='')
    contato_administradora = models.CharField(
        _('Contato Administradora'), blank=True, max_length=128, default='')
    regras_mudanca = models.CharField(
        _('Regras para mudanças'), blank=True, max_length=128, default='')
    portaria = models.CharField(
        choices=TIPO_PORTARIA, max_length=16,
        default='', blank=True)
    # Portaria mudam com o passar do tempo,
    # É importante saber quando este campo foi atualizado
    portaria_atualizada_em = models.DateTimeField(
        'Data da atualização da portaria',
        null=True, blank=True)

    objects = ManagerBase()

    class Meta:
        verbose_name = _("Condomínio")
        verbose_name_plural = _("Condomínios")
        ordering = ('nome', )

    def __str__(self):
        return self.nome

    @property
    def elevador(self):
        return "Sim" if self.tem_elevador else "Não"


@python_2_unicode_compatible
class Imovel(ComEndereco):
    STATUS = Choices(('novo', _('Novo')),
                     ('publicado', _('Publicado')),
                     ('arquivado', _('Arquivado')), )
    TIPO_IMOVEL = Choices(('apartamento', _('Apartamento')),
                          ('casa', _('Casa')),
                          ('terreno', _('Terreno')),
                          ('areaurbana', _('Área urbana')),
                          ('chacara', _('Chácara/Sítio')),
                          ('loja', _('Loja/Ponto')),
                          ('sala', _('Sala/Consultório')),
                          ('galpao', _('Galpão/Depósito')),
                          ('edificio', _('Edifício/Prédio')), )
    LOCAL_CHAVE = Choices(('imobiliaria', _('Imobiliaria')),
                          ('portaria', _('Portaria')),
                          ('proprietario', _('Proprietário')),
                          ('outro', _('Outro')), )
    TIPO_VARANDA = Choices(('', _('-')),
                           ('sem', _('Sem Varanda/Sacada')),
                           ('varanda', _('Com Varanda')),
                           ('varandaG', _('Com Varanda Gourmet')),
                           ('sacada', _('Com Sacada')),
                           ('terraco', _('Com Terraço')),
                           ('terracoG', _('Com Terraço Gourmet')), )

    slug = models.SlugField(max_length=128, blank=True, default='')
    data_cadastro = models.DateTimeField(_('data cadastro'), auto_now_add=True)
    atualizado_em = models.DateTimeField(_('atualizado em'), auto_now=True)
    status = models.CharField(choices=STATUS, default=STATUS.novo,
                              max_length=16)
    imovel_ref = models.CharField(_('Referência'),
                                  max_length=32, default='')
    eh_para_locacao = models.BooleanField(_('Para locação'), default=False)
    valor_locacao = models.DecimalField(
        _('Valor locação'), max_digits=12, decimal_places=2, default=0.00)
    eh_para_venda = models.BooleanField(_('Para venda'), default=False)
    valor_venda = models.DecimalField(
        _('Valor venda'), max_digits=12, decimal_places=2, default=0.00)
    valor_condominio = models.DecimalField(
        _('Valor condomínio'), max_digits=12, decimal_places=2, default=0.00)
    valor_iptu = models.DecimalField(
        _('Valor IPTU'), max_digits=12, decimal_places=2, default=0.00)
    tipo_imovel = models.CharField(
        _('Tipo do imóvel'), max_length=16, choices=TIPO_IMOVEL)
    eh_apto_duplex = models.BooleanField(_('Duplex'), default=False)
    eh_apto_triplex = models.BooleanField(_('Triplex'), default=False)
    eh_apto_cobertura = models.BooleanField(_('Cobertura'), default=False)
    eh_casa_terrea = models.BooleanField(_('Terrea'), default=False)
    eh_casa_edicula = models.BooleanField(_('Edícula'), default=False)
    eh_casa_sobreloja = models.BooleanField(_('Sobreloja'), default=False)
    eh_casa_sobrado = models.BooleanField(_('Sobrado'), default=False)
    eh_casa_geminada = models.BooleanField(_('Geminada'), default=False)
    eh_kitnet = models.BooleanField(_('Kitnet'), default=False)
    eh_imovel_novo = models.BooleanField(_('Imóvel novo'), default=False)
    eh_comercial = models.BooleanField(_('Imóvel comercial'), default=False)
    dormitorios = models.PositiveSmallIntegerField(
        _('Nro. Dormitórios'), blank=True, default=0)
    banheiros = models.PositiveSmallIntegerField(
        _('Nro. Banheiros'), blank=True, default=0)
    suites = models.PositiveSmallIntegerField(
        _('Nro. Suítes'), blank=True, default=0)
    vagas_garagem = models.PositiveSmallIntegerField(
        _('Vagas Garagem'), blank=True, default=0)
    area_construida = models.PositiveIntegerField(
        _('Área Construída'), blank=True, default=0)
    area_terreno = models.PositiveIntegerField(
        _('Área Terreno'), blank=True, default=0)
    dimensoes_terreno = models.CharField(
        _('Dimensões Terreno'), blank=True, max_length=64, default='')
    descricao_imovel = models.TextField(
        _('Descrição do imóvel'), blank=True, default='')
    descricao_comodos = models.TextField(
        _('Descrição cômodos'), blank=True, default='')
    esta_ocupado = models.BooleanField(_('Ocupado'), default=False)
    esta_mobiliado = models.BooleanField(_('Mobiliado'), default=False)
    esta_com_placa = models.BooleanField(_('Com placa'), default=False)
    local_chave = models.CharField(choices=LOCAL_CHAVE, max_length=16,
                                   default=LOCAL_CHAVE.proprietario)
    local_chave_observacao = models.CharField(
        _('Local da chave observação'), blank=True, max_length=128, default='')
    observacoes_internas = models.TextField(
        _('Observações internas'), blank=True, default='')
    forma_de_pagamentos = models.ManyToManyField(FormaDePagamento, blank=True)
    outra_forma_de_pagamento = models.CharField(
        _('Outras formas de pagamentos'), blank=True, max_length=128, default='')
    areadelazer_imovel = models.ManyToManyField(
        AreaDeLazer, blank=True, verbose_name=_('do imóvel'))
    proprietario = models.ForeignKey(
        Proprietario, verbose_name=_('Proprietário'),
        null=True, on_delete=models.SET_NULL)
    condominio = models.ForeignKey(
        Condominio, verbose_name=_('Condomínio'), null=True, blank=True)
    corretores = models.ManyToManyField(
        Corretor, blank=True, verbose_name=_('Corretores'))
    indicado_por = models.CharField(
        _('Indicado por'), blank=True, max_length=128, default='')
    foto_principal = models.ForeignKey(
        "Foto", verbose_name=_('Foto Principal'),
        related_name="fotos", null=True, blank=True, on_delete=models.SET_NULL)
    # Nao envia imovel para Zap, Viva Real entre outros
    nao_exportar_para_portais = models.BooleanField(
        _('Não exportar para portais imobiliarios'),
        default=False)
    tipo_varanda = models.CharField(
        choices=TIPO_VARANDA, max_length=16,
        default='', blank=True)

    objects = models.Manager()
    objects_geral = ImovelManagerBase()
    para_venda = ImovelVendasManager()
    para_locacao = ImovelLocacoesManager()

    class Meta:
        get_latest_by = 'data_cadastro'
        verbose_name = _("Imóvel")
        verbose_name_plural = _("Imóveis")

    def __str__(self):
        return self.imovel_ref

    def atualizar_contador_de_bairro(self):
        if not self.bairro:
            return
        contador_venda = Imovel.para_venda.publicados().por_tipo_imovel(
            self.tipo_imovel).por_bairro(self.bairro).count()
        contador_locacao = Imovel.para_locacao.publicados().por_tipo_imovel(
            self.tipo_imovel).por_bairro(self.bairro).count()
        contador, created = BairroComImoveis.objects.get_or_create(bairro=self.bairro, tipo_imovel=self.tipo_imovel)
        contador.cidade = self.cidade
        contador.regiao = self.regiao
        contador.contador_venda = contador_venda
        contador.contador_locacao = contador_locacao
        contador.save()

    def save(self, *args, **kwargs):
        if not self.imovel_ref:
            try:
                ultima_ref = Imovel.objects.latest().imovel_ref
            except:
                ultima_ref = 0
            self.imovel_ref = str(int(ultima_ref) + 1)
        if not self.slug and self.bairro and self.imovel_ref:
            self._atualizar_slug()

        self.atualizar_contador_de_bairro()
        foto_principal = self.fotos_list.filter(eh_principal=True)
        if foto_principal:
            self.foto_principal = foto_principal[0]
        super(Imovel, self).save(*args, **kwargs)

    def get_absolute_url(self):
        tipo_interesse = 'comprar' if self.eh_para_venda else 'alugar'
        if not self.slug:
            return reverse('imoveis.novo.imovel.passo2',
                           kwargs={'pk': self.id})
        url = "{0}?interesse={1}".format(
            reverse('ibuscador.imovel.detalhe',
                    kwargs={'slug': self.slug, 'pk': self.id}),
            tipo_interesse)
        return url

    def _atualizar_slug(self):
        self.slug = slugify('{0}-{1}-{2}-{3}'.format(
            self.tipo_imovel, self.bairro.descricao,
            self.cidade.nome, self.imovel_ref))

    def descricao_imovel_as_list(self):
        return self.descricao_imovel.split('\n')

    def descricao_comodos_as_list(self):
        return self.descricao_comodos.split('\n')

    # STATUS
    @property
    def esta_publicado(self):
        return self.status == Imovel.STATUS.publicado

    @property
    def esta_arquivado(self):
        return self.status == Imovel.STATUS.arquivado

    @property
    def eh_novo(self):
        return self.status == Imovel.STATUS.novo

    # TIPO_IMOVEL
    @property
    def tipo_imovel_verbose(self):
        return Imovel.TIPO_IMOVEL[self.tipo_imovel]

    @property
    def eh_apartamento(self):
        return self.tipo_imovel == Imovel.TIPO_IMOVEL.apartamento

    @property
    def eh_casa(self):
        return self.tipo_imovel == Imovel.TIPO_IMOVEL.casa

    @property
    def eh_terreno(self):
        return self.tipo_imovel == Imovel.TIPO_IMOVEL.terreno

    @property
    def eh_areaurbana(self):
        return self.tipo_imovel == Imovel.TIPO_IMOVEL.areaurbana

    @property
    def eh_chacara(self):
        return self.tipo_imovel == Imovel.TIPO_IMOVEL.chacara

    @property
    def eh_loja(self):
        return self.tipo_imovel == Imovel.TIPO_IMOVEL.loja

    @property
    def eh_sala(self):
        return self.tipo_imovel == Imovel.TIPO_IMOVEL.sala

    @property
    def eh_galpao(self):
        return self.tipo_imovel == Imovel.TIPO_IMOVEL.galpao

    @property
    def eh_edificio(self):
        return self.tipo_imovel == Imovel.TIPO_IMOVEL.edificio

    @property
    def tem_area_total(self):
        """ alguns tipos de imoveis devem levar em conta o tamanho
            do terreno e NAO a area construida
        """
        if self.eh_edificio or self.eh_terreno or self.eh_chacara or self.eh_galpao:
            return True
        return False

    @property
    def valor_locacao_total(self):
        return self.valor_locacao + self.valor_condominio

    @property
    def media_metro_quadrado(self):
        if self.tem_area_total and self.area_terreno:
            return int(self.valor_venda / self.area_terreno)
        elif not self.valor_venda or not self.area_construida:
            return 0
        return int(self.valor_venda / self.area_construida)

    @property
    def area_total(self):
        if self.tem_area_total:
            return self.area_terreno
        return self.area_construida

    @property
    def suites_verbose(self):
        if self.suites > 0:
            return self.suites
        else:
            return 0

    @property
    def titulo(self):
        descricao = ''
        if not self.tipo_imovel:
            return 'Indefinido'
        if self.tipo_imovel == Imovel.TIPO_IMOVEL.apartamento:
            descricao = 'Cobertura ' if self.eh_apto_cobertura else ''
            if self.eh_apto_duplex:
                descricao += 'Duplex '
            elif self.eh_apto_triplex:
                descricao += 'Triplex '
            descricao += 'mobiliado ' if self.esta_mobiliado else ''
        elif self.tipo_imovel == Imovel.TIPO_IMOVEL.casa:
            if self.eh_casa_sobrado:
                descricao = 'Sobrado '
            elif self.eh_casa_edicula:
                descricao = 'Edicula '
            elif self.eh_casa_sobreloja:
                descricao = 'Sobreloja '
            descricao += 'mobiliada ' if self.esta_mobiliado else ''
            descricao += 'em condominio ' if self.condominio else ''
        descricao += 'Comercial ' if self.eh_comercial else ''
        return '{0} {1}'.format(Imovel.TIPO_IMOVEL[self.tipo_imovel],
                                descricao)

    @property
    def ocupado(self):
        return 'Sim' if self.esta_ocupado else 'Não'

    @property
    def mobiliado(self):
        return 'Sim' if self.esta_mobiliado else 'Não'

    @property
    def add_tipo_imovel_class(self):
        try:
            titulo = normalize('NFKD', self.titulo.lower().decode('utf-8'))
            return titulo.encode('ASCII', 'ignore')
        except:
            return ''

    @property
    def fotos_list(self):
        return Foto.objects.filter(imovel=self).order_by("ordem")

    @property
    def historico_list(self):
        return HistoricoDeImovel.objects.filter(imovel=self)

    @property
    def googlemaps(self):
        endereco = "{} {} {}".format(self.logradouro, self.numero, self.cidade)
        return "https://www.google.com.br/maps/place/{}".format(endereco.replace(" ", "+"))


@python_2_unicode_compatible
class BairroComImoveis(models.Model):
    tipo_imovel = models.CharField(max_length=16, choices=Imovel.TIPO_IMOVEL, default='')
    bairro = models.ForeignKey(Bairro, verbose_name=_('Bairro'))
    cidade = models.ForeignKey(Cidade, verbose_name=_('Cidade'),
                               null=True, blank=True)
    regiao = models.ForeignKey(Regiao, verbose_name=_('Região'),
                               null=True, blank=True)
    contador_venda = models.PositiveSmallIntegerField(default=0)
    contador_locacao = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = _("Bairro com imóveis")
        verbose_name_plural = _("Bairros com imóveis")

    def __str__(self):
        return '{0}'.format(self.bairro.nome, )


@python_2_unicode_compatible
class Foto(models.Model):
    imovel = models.ForeignKey(Imovel, verbose_name=_('Imovel'))
    descricao = models.CharField(_('descrição'), max_length=255,
                                 null=True, blank=True)
    picture = models.ImageField(
        _('picture'), upload_to='imovel_fotos/%Y/%m', blank=True, default='')
    picture_cropping = ImageRatioField('picture', '1024x632', free_crop=True)
    ordem = models.IntegerField(blank=True, default=1, null=True)
    eh_principal = models.BooleanField(_('Foto Principal'), default=False)

    def _auto_incremente_ordem_foto(self):
        if not self.id:
            ultima_imagem = self.imovel.fotos_list.last()
            if ultima_imagem is not None:
                return int(self.imovel.fotos_list.last().ordem) + 1
            return 1
        return self.ordem

    def save(self, *args, **kwargs):
        self.ordem = self._auto_incremente_ordem_foto()
        super(Foto, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('foto')
        verbose_name_plural = _('fotos')

    def __str__(self):
        return '{0}'.format(self.descricao or 'sem descrição')


@python_2_unicode_compatible
class DescricaoImovel(models.Model):
    """
    Entidade auxiliar para ajudar no autocomplete para preencher o
    campo descrição do imovel. Ex. PISO DE MADEIRA, SOL DA MANHA
    """
    tipo_imovel = models.CharField(
        _('Tipo do imóvel'), max_length=16,
        choices=Imovel.TIPO_IMOVEL, null=True, blank=True)
    descricao = models.CharField(_('descrição'), max_length=255,
                                 null=True, blank=True)

    class Meta:
        ordering = ['descricao']

    def __str__(self):
        return '{0}'.format(self.descricao or 'sem descrição')


@python_2_unicode_compatible
class DescricaoComodo(models.Model):
    """
    Entidade auxiliar para ajudar no autocomplete para preencher o
    campo descrição do comodo. Ex. Sala de estar, Cozinha com armário...
    """
    tipo_imovel = models.CharField(
        _('Tipo do imóvel'), max_length=16,
        choices=Imovel.TIPO_IMOVEL, null=True, blank=True)
    descricao = models.CharField(_('descrição'), max_length=255,
                                 null=True, blank=True)

    def __str__(self):
        return '{0}'.format(self.descricao or 'sem descrição')


@python_2_unicode_compatible
class HistoricoDeImovel(models.Model):
    """
    Informações relevantes sobre as alterações do cadastro de imoveis
    """
    imovel = models.ForeignKey(Imovel, verbose_name=_('Imovel'), related_name='historicoalteracoes')
    data = models.DateTimeField()
    usuario = models.ForeignKey(
        User, verbose_name=_('Usuario'), related_name='usuario',
        null=True, blank=True)
    conteudo = models.CharField(
        'conteudo', max_length=1024, default='')

    class Meta:
        verbose_name = 'historico'
        verbose_name_plural = 'historicos'
        ordering = ['-data']

    def __str__(self):
        return '{0}: {1}'.format(
            self.usuario, self.conteudo)


from .signals import organizar_fotos