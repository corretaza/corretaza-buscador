def trocar_ordem_fotos_mesma_ordem(instance, fotos_imovel):
    '''Trocar ordem das fotos com valores iguais, para seguir a seguencia crescente dos numero'''
    mesma_ordem = fotos_imovel.filter(ordem=instance.ordem).exclude(id=instance.id)
    if mesma_ordem:
        mesma_ordem = iter(mesma_ordem)
        ordens_das_fotos = fotos_imovel.values("ordem")
        ordens_ausentes = set(range(1, ordens_das_fotos.count()+1)) - \
                          {values['ordem'] for values in ordens_das_fotos}
        while mesma_ordem and ordens_ausentes:
            foto = mesma_ordem.next()
            foto.ordem = ordens_ausentes.pop()
            foto.save()


def mudar_foto_principal(instance, fotos_imovel):
    if instance.eh_principal:
        fotos_principais = fotos_imovel.filter(eh_principal=True).exclude(id=instance.id)
        for foto in fotos_principais:
            foto.eh_principal = False
            foto.save()