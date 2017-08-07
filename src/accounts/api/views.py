from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser

from .serializers import UserCreateSerializer


# Create your views here.
User = get_user_model()


class UserCreateAPIView(CreateAPIView):
	permission_classes = [IsAdminUser]
	queryset = User.objects.all()
	serializer_class = UserCreateSerializer