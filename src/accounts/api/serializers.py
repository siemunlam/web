# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.serializers import CharField, ChoiceField, CurrentUserDefault, EmailField, ModelSerializer, ValidationError
from rest_framework.validators import UniqueValidator

from medicos.models import Medico
from accounts.constants import PERFIL_CHOICES
from accounts.helper_func import can_create, get_profile_from_id, get_profile_from_name

# Create your serializers here.
User = get_user_model()

class UserCreateSerializer(ModelSerializer):
	perfil = ChoiceField(choices=PERFIL_CHOICES)
	pwd2 = CharField(label=u'Reingreso de contraseña', style={'input_type': 'password'}, write_only=True)

	class Meta:
		model = User
		fields = ['username', 'perfil', 'first_name', 'last_name', 'email', 'password', 'pwd2']
		extra_kwargs = {
			'username': {'help_text': '', 'label': 'Usuario', 'max_length': 30, 'style': {'placeholder': 'Ej: miNombreDeUsuario'}},
			'first_name': {'label': 'Nombre', 'style': {'placeholder': 'Ej: Juan'}},
			'last_name': {'label': 'Apellido', 'style': {'placeholder': u'Ej: Pérez'}},
			'email': {
				'allow_blank': False,
				'label': u'Dirección de email',
				'required': True,
				'style': {'placeholder': 'Ej: miCorreo@server.com'},
				'validators': [UniqueValidator(queryset=User.objects.all())]
			},
			'password': {'label': u'Contraseña', 'style': {'input_type': 'password'}, 'write_only': True}
		}
	
	def validate_email(self, value):
		user_qs = User.objects.filter(email=value)
		if user_qs.exists():
			raise ValidationError('Ya existe un usuario con ese email')
		return value
	
	def validate(self, attrs):
		if not attrs.get('password') == attrs.get('pwd2'):
			raise ValidationError(u'El reingreso no coincide con la contraseña.')
		return attrs

	def create(self, validated_data):
		user_obj = User(username=validated_data['username'], email=validated_data['email'], first_name=validated_data['first_name'], last_name=validated_data['last_name'])
		user_obj.set_password(validated_data['password'])
		user_obj.save()
		group = get_profile_from_id(validated_data['perfil'])
		current_user_group = self.context['request'].user.groups.first().name
		if not can_create(get_profile_from_name(current_user_group)['id'], group['id']):
			raise ValidationError(u'No posee autorización para crear un usuario con perfil \"%s\"' %group['name'])
		user_obj.groups.add(Group.objects.get(name=group['group_name']))
		return validated_data


class UserLoginSerializer(ModelSerializer):
	username = CharField(label='Usuario')

	class Meta:
		model = User
		fields = ['username', 'password']
		extra_kwargs = { 'password': {'style': {'input_type': 'password'}, 'write_only': True} }
	
	def validate(self, data):
		try:
			user = User.objects.get(username=data['username'])
		except User.DoesNotExist as e:
			raise ValidationError('Credenciales incorrectas.')
		if Medico.objects.filter(usuario=user).exists():
			raise ValidationError(u'Esta API no permite loguear médicos.')
		if not user.check_password(data['password']):
			raise ValidationError('Credenciales incorrectas.')
		return data


class UserRetrieveUpdateDestroySerializer(ModelSerializer):
	class Meta:
		model = User
		fields = ['username', 'email', 'first_name', 'last_name', 'groups', 'last_login', 'date_joined']
		read_only_fields = ['last_login', 'date_joined', 'username']
		depth = 1


class UserPwdUpdateSerializer(ModelSerializer):
	new_pwd = CharField(label=u'Nueva contraseña', style={'input_type': 'password'}, write_only=True)
	re_new_pwd = CharField(label=u'Reingrese la nueva contraseña', style={'input_type': 'password'}, write_only=True)
	
	class Meta:
		model = User
		fields = ['password', 'new_pwd', 're_new_pwd']
		extra_kwargs = {
			'password': {'style': {'input_type': 'password'}, 'write_only': True}
		}
	
	def validate(self, data):
		if not data.get('re_new_pwd') == data.get('new_pwd'):
			raise ValidationError(u'El reingreso no coincide con la nueva contraseña.')
		return data

	def update(self, instance, validated_data):
		if not instance.check_password(validated_data.get('password')):
			raise ValidationError(u'La contraseña actual ingresada es incorrecta.')
		instance.set_password(validated_data.get('new_pwd'))
		instance.save()
		return instance