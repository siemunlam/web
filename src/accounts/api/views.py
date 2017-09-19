from django.contrib.auth import get_user_model, login, logout
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from .serializers import UserCreateSerializer, UserLoginSerializer, UserRetrieveUpdateDestroySerializer
from medicos.models import Medico
from accounts.api.constants import MEDICO


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