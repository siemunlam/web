# -*- coding: utf-8 -*-

## Profile / Group declaration constants
OPERADOR = {
    'id': 1,
    'name': 'Operador',
    'group_name': 'operadores'
}
SUPERVISOR = {
    'id': 2,
    'name': 'Supervisor',
    'group_name': 'supervisores'
}
DIRECTIVO = {
    'id': 3,
    'name': 'Directivo',
    'group_name': 'directivos'
}
MEDICO = {
    'id': 4,
    'name': u'Médico',
    'group_name': u'médicos'
}

PERFIL_CHOICES = (
    (OPERADOR['id'], OPERADOR['name']),
    (SUPERVISOR['id'], SUPERVISOR['name']),
    (DIRECTIVO['id'], DIRECTIVO['name'])
)