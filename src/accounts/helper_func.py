from accounts.api.constants import DIRECTIVO, MEDICO, OPERADOR, SUPERVISOR


def es_directivo(user):
    return user.groups.filter(name=DIRECTIVO['group_name']).exists()

def es_medico(user):
    return user.groups.filter(name=MEDICO['group_name']).exists()

def es_supervisor(user):
    return user.groups.filter(name=SUPERVISOR['group_name']).exists()

def posee_usuarios_a_cargo(user):
    return es_directivo(user) | es_supervisor(user)
