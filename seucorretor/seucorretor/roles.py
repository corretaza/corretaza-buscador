from rolepermissions.roles import AbstractUserRole
from rolepermissions.shortcuts import revoke_permission, grant_permission


class Gerente(AbstractUserRole):
    available_permissions = {
        'acesso_completo': True,
        'alterar_imovel': True,
    }


class Corretor(AbstractUserRole):
    available_permissions = {
        'acesso_completo': False,
        'alterar_imovel': True,
    }


class Estagiario(AbstractUserRole):
    available_permissions = {
        'acesso_completo': False,
        'alterar_imovel': False,
    }


def update_roles(user, pode_alterar_imovel=True):
    """
    Por padrao corretores podem alterar imoveis,
    porem alguns podem ter acesso bloqueado
    """
    if not pode_alterar_imovel:
        revoke_permission(user, 'alterar_imovel')
        return False
    else:
        grant_permission(user, 'alterar_imovel')
        return True
