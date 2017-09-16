# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.serializers import CharField, CurrentUserDefault, EmailField, HiddenField, ModelSerializer, ReadOnlyField, FloatField
from rest_framework.validators import UniqueValidator

from accounts.api.serializers import UserRetrieveUpdateDestroySerializer
from medicos.models import Medico
from accounts.api.constants import MEDICO
from auxilios.api.extra_func import generarAsignacion

# Create your serializers here.
User = get_user_model()

class MedicoCreateSerializer(ModelSerializer):
	apellido = CharField(max_length=50, style={'placeholder': 'Ej: Robles'})
	nombre = CharField(max_length=50, style={'placeholder': 'Ej: Miguel'})
	email = EmailField(style={'placeholder': 'Ej: micorreo@algo.com'})
	estado = ReadOnlyField(source='get_estado_display')
	usuario = HiddenField(default=None)
	generador = HiddenField(default=CurrentUserDefault())

	class Meta:
		model = Medico
		fields = ('dni', 'matricula', 'apellido', 'nombre', 'email', 'estado', 'telefono', 'usuario', 'generador')
		extra_kwargs = {
			'dni': {'style': {'placeholder': 'Ej: 12345678', 'autofocus': True}},
			'matricula': {'label': u'Matrícula', 'style': {'placeholder': 'Ej: 123456'}},
			'telefono': {'label': u'Teléfono', 'style': {'placeholder': 'Ej: 11 1234 5678'}}
		}
	
	def create(self, validated_data):
		user_obj = User(username=validated_data['matricula'],
						first_name=validated_data['nombre'],
						last_name=validated_data['apellido'],
						email=validated_data['email'])
		user_obj.set_password(validated_data['matricula'])
		user_obj.save()
		user_obj.groups.add(Group.objects.get(name=MEDICO['group_name']))
		Medico.objects.create(dni=validated_data['dni'], matricula=validated_data['matricula'], telefono=validated_data['telefono'], usuario=user_obj, generador=validated_data['generador'])
		return validated_data


class MedicoDetailSerializer(ModelSerializer):
	usuario = UserRetrieveUpdateDestroySerializer()
	estado = ReadOnlyField(source='get_estado_display')
	generador = ReadOnlyField(source='generador.username')

	class Meta:
		model = Medico
		fields = ['dni', 'matricula', 'usuario', 'telefono', 'estado', 'fcm_code', 'generador', 'latitud_gps', 'longitud_gps']


class MedicoLogoutSerializer(ModelSerializer):
	class Meta:
		model = Medico
		fields = ['dni', 'matricula', 'estado', 'fcm_code', 'latitud_gps', 'longitud_gps']
		extra_kwargs = {
			'dni': {'read_only': True},
			'matricula': {'read_only': True},
			'estado': {'read_only': True},
			'fcm_code': {'read_only': True},
			'latitud_gps': {'read_only': True},
			'longitud_gps': {'read_only': True}
		}


class MedicoUpdateSerializer(ModelSerializer):
	apellido = CharField(max_length=50, style={'placeholder': 'Ej: Robles'})
	nombre = CharField(max_length=50, style={'placeholder': 'Ej: Miguel'})
	email = EmailField(style={'placeholder': 'Ej: micorreo@algo.com'})

	class Meta:
		model = Medico
		fields = ['matricula', 'apellido', 'nombre', 'email', 'telefono']
		extra_kwargs = {
			'matricula': {'label': u'Matrícula', 'style': {'placeholder': 'Ej: 123456', 'autofocus': True}},
			'telefono': {'label': u'Teléfono', 'style': {'placeholder': 'Ej: 11 1234 5678'}}
		}
	
	def update(self, instance, validated_data):
		instance = super(MedicoUpdateSerializer, self).update(instance, validated_data)
		instance.usuario.last_name = validated_data.get('apellido', instance.usuario.last_name)
		instance.usuario.first_name = validated_data.get('nombre', instance.usuario.first_name)
		instance.usuario.email = validated_data.get('email', instance.usuario.email)
		instance.usuario.save()
		return instance


class MedicoCambioEstadoSerializer(ModelSerializer):
	class Meta:
		model = Medico
		fields = ['estado',]
	
	def update(self, instance, validated_data):
		nuevo_estado = validated_data['estado']
		instance.estado = nuevo_estado
		instance.save()
		if nuevo_estado == Medico.DISPONIBLE:
			generarAsignacion()
		return instance


class MedicoActualizarGPSSerializer(ModelSerializer):
	class Meta:
		model = Medico
		fields = ['latitud_gps', 'longitud_gps']


class MedicoActualizarFCMSerializer(ModelSerializer):
	class Meta:
		model = Medico
		fields = ['fcm_code',]
