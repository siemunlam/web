# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.serializers import CharField, ChoiceField, EmailField, ModelSerializer, ValidationError
from rest_framework.validators import UniqueValidator

from medicos.models import Medico
from .constants import OPERADOR, SUPERVISOR, DIRECTIVO


# Create your serializers here.
User = get_user_model()

class UserCreateSerializer(ModelSerializer):
	PERFIL_CHOICES = (
		(OPERADOR['id'], OPERADOR['name']),
		(SUPERVISOR['id'], SUPERVISOR['name']),
		(DIRECTIVO['id'], DIRECTIVO['name'])
	)
	# email2 = EmailField(label='Reingreso de email')
	perfil = ChoiceField(choices=PERFIL_CHOICES)

	class Meta:
		model = User
		fields = ['username', 'perfil', 'first_name', 'last_name', 'email', 'password']
		extra_kwargs = {
			'username': {'help_text': '', 'label': 'Nombre de usuario', 'style': {'placeholder': 'Ej: miNombreDeUsuario'}},
			'first_name': {'label': 'Nombre', 'style': {'placeholder': 'Ej: Juan'}},
			'last_name': {'label': 'Apellido', 'style': {'placeholder': u'Ej: Pérez'}},
			'email': {
				'allow_blank': False,
				'label': u'Dirección de email',
				'required': True,
				'style': {'placeholder': 'Ej: miCorreo@server.com'},
				'validators': [UniqueValidator(queryset=User.objects.all())]
			},
			'password': {'label': u'Contraseña', 'style': {'input_type': 'password'}, 'write_only': True},
		}
	
	# def validate_email(self, value):
	# 	user_qs = User.objects.filter(email=value)
	# 	if user_qs.exists():
	# 		raise ValidationError('Ya existe un usuario con ese email')
	# 	return value

	# def validate_email2(self, value):
	# 	data = self.get_initial()
	# 	if data.get('email') != value:
	# 		raise ValidationError('Los emails no coinciden')
	# 	return value
	
	def create(self, validated_data):
		user_obj = User(username=validated_data['username'], email=validated_data['email'], first_name=validated_data['first_name'], last_name=validated_data['last_name'])
		user_obj.set_password(validated_data['password'])
		user_obj.save()
		group_name = None
		if validated_data['perfil'] == OPERADOR['id']:
			group_name = OPERADOR['group_name']
		elif validated_data['perfil'] == SUPERVISOR['id']:
			group_name = SUPERVISOR['group_name']
		elif validated_data['perfil'] == DIRECTIVO['id']:
			group_name = DIRECTIVO['group_name']
		user_obj.groups.add(Group.objects.get(name=group_name))
		return validated_data


class UserLoginSerializer(ModelSerializer):
	username = CharField(label='Nombre de usuario')
	password = CharField(label='Contraseña', style={'input_type': 'password'})
	
	class Meta:
		model = User
		fields = ['username', 'password']
		extra_kwargs = {'password': {'write_only': True}}
	
	def validate(self, data):
		try:
			user = User.objects.get(username=data['username'])
		except Exception as e:
			raise ValidationError('Credenciales incorrectas.')
		if Medico.objects.filter(usuario=user).exists():
			raise ValidationError(u'Ésta API no permite loguear médicos.')
		if not user.check_password(data['password']):
			raise ValidationError('Credenciales incorrectas.')
		return data


class UserDetailSerializer(ModelSerializer):
	class Meta:
		model = User
		fields = ['username', 'email', 'first_name', 'last_name', 'groups', 'last_login', 'date_joined']
		extra_kwargs = {'last_login': {'read_only': True}, 'date_joined': {'read_only': True}}
		depth = 1


class UserRetrieveUpdateDestroySerializer(ModelSerializer):
	class Meta:
		model = User
		fields = ['username', 'email', 'first_name', 'last_name', 'groups', 'last_login', 'date_joined']
		extra_kwargs = {'last_login': {'read_only': True}, 'date_joined': {'read_only': True}}
		depth = 1
		

class UserUpdateSerializer(ModelSerializer):
	class Meta:
		model = User
		fields = ['email', 'first_name', 'last_name']