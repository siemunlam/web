# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model, login, logout
from rest_framework.exceptions import NotAcceptable
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from .serializers import UserCreateSerializer, UserLoginSerializer, UserRetrieveUpdateDestroySerializer
from medicos.models import Medico
from accounts.constants import MEDICO
from accounts.helper_func import can_delete, get_profile_from_name


# Create your views here.
User = get_user_model()


class UserCreateAPIView(CreateAPIView):
	permission_classes = [IsAuthenticated]
	queryset = User.objects.all()
	serializer_class = UserCreateSerializer


class UserListAPIView(ListAPIView):
	permission_classes = [IsAuthenticated]
	queryset = User.objects.exclude(groups__name__in=[MEDICO['group_name'],]).order_by('username')
	serializer_class = UserRetrieveUpdateDestroySerializer


class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
	permission_classes = [IsAuthenticated]
	queryset = User.objects.all()
	serializer_class = UserRetrieveUpdateDestroySerializer

	def get_object(self):
		return User.objects.get(username = self.kwargs['username'])

	def delete(self, request, *args, **kwargs):
		if self.request.user == self.get_object():
			raise NotAcceptable(u'No se permite borrar su propio usuario.')
		group = self.get_object().groups.first().name
		current_user_group = self.request.user.groups.first().name
		if not can_delete(get_profile_from_name(current_user_group)['id'], get_profile_from_name(group)['id']):
			raise NotAcceptable(u'No posee autorización para borrar un usuario con perfil \"%s\".' %self.get_object().groups.first().name)
		return self.destroy(request, *args, **kwargs)


class UserLoginAPIView(APIView):
	permission_classes = [AllowAny]
	serializer_class = UserLoginSerializer

	def post(self, request, *args, **kwargs):
		data = request.data
		serializer = UserLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			new_data = serializer.data
			user = User.objects.get(username=new_data['username'])
			login(request, user)
			return Response(new_data, status=HTTP_200_OK)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)