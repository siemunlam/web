from accounts.constants import DIRECTIVO, MEDICO, OPERADOR, SUPERVISOR, PROFILES

def get_profile_from_id(id, profiles=PROFILES):
	for profile in profiles:
		if profile['id'] == id:
			return profile
	return None

def get_profile_from_name(group_name, profiles=PROFILES):
	for profile in profiles:
		if profile['group_name'] == group_name:
			return profile
	return None

# def get_perfil_choices(user_group, profiles):
# 	choices = list()
# 	perfil = get_profile(user_group, profiles)
# 	for can_create in perfil['can_create']:
# 		choices.append((
# 			get_profile(can_create, profiles)['id'],
# 			get_profile(can_create, profiles)['name']))

def can_create(user_group_id, create_group_id, profiles=PROFILES):
	if create_group_id in get_profile_from_id(user_group_id, profiles)['can_create']:
		return True
	return False

def can_delete(user_group_id, delete_group_id, profiles=PROFILES):
	if delete_group_id in get_profile_from_id(user_group_id, profiles)['can_delete']:
		return True
	return False

def es_directivo(user):
	return user.groups.filter(name=DIRECTIVO['group_name']).exists()

def es_medico(user):
	return user.groups.filter(name=MEDICO['group_name']).exists()

def es_supervisor(user):
	return user.groups.filter(name=SUPERVISOR['group_name']).exists()

def posee_usuarios_a_cargo(user):
	return es_directivo(user) | es_supervisor(user)