# -*- coding: utf-8 -*-

## Profile / Group declaration constants
OPERADOR = {
	'id': 1,
	'name': 'Operador',
	'group_name': 'operadores',
	'can_create': [],
	'can_delete': []
}
SUPERVISOR = {
	'id': 2,
	'name': 'Supervisor',
	'group_name': 'supervisores',
	'can_create': [1, 4],
	'can_delete': [1, 4]
}
DIRECTIVO = {
	'id': 3,
	'name': 'Directivo',
	'group_name': 'directivos',
	'can_create': [1, 2, 4],
	'can_delete': [1, 2, 4]
}
MEDICO = {
	'id': 4,
	'name': u'Médico',
	'group_name': u'médicos',
	'can_create': [],
	'can_delete': []
}

PROFILES = [OPERADOR, SUPERVISOR, DIRECTIVO, MEDICO]

PERFIL_CHOICES = (
	(OPERADOR['id'], OPERADOR['name']),
	(SUPERVISOR['id'], SUPERVISOR['name']),
	(DIRECTIVO['id'], DIRECTIVO['name'])
)