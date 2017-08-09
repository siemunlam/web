from django.contrib.auth import get_user_model
from rest_framework.serializers import CharField, EmailField, ModelSerializer, ValidationError


# Create your serializers here.
User = get_user_model()


class UserCreateSerializer(ModelSerializer):
	email = EmailField(label=u'Dirección de email')
	email2 = EmailField(label='Reingreso de email')

	class Meta:
		model = User
		fields = ['username', 'email', 'email2', 'password']
		extra_kwargs = {'password': {'write_only': True}}
	
	def validate_email(self, value):
		user_qs = User.objects.filter(email=value)
		if user_qs.exists():
			raise ValidationError('Ya existe un usuario con ese email')
		return value

	def validate_email2(self, value):
		data = self.get_initial()
		if data.get('email') != value:
			raise ValidationError('Los emails no coinciden')
		return value
	
	def create(self, validated_data):
		user_obj = User(username=validated_data['username'], email=validated_data['email'])
		user_obj.set_password(validated_data['password'])
		user_obj.save()
		return validated_data


class UserDetailSerializer(ModelSerializer):
	class Meta:
		model = User
		fields = ['username', 'email', 'first_name', 'last_name', 'groups', 'last_login', 'date_joined']
		extra_kwargs = {'last_login': {'read_only': True}, 'date_joined': {'read_only': True}}
		depth = 1


class UserUpdateSerializer(ModelSerializer):
	class Meta:
		model = User
		fields = ['email', 'first_name', 'last_name']