# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView, TemplateView

from accounts.api.serializers import UserCreateSerializer, UserLoginSerializer, UserRetrieveUpdateDestroySerializer
from accounts.helper_func import posee_usuarios_a_cargo
from medicos.models import Medico

# Create your views here.
class LoginView(TemplateView):
	success_url = reverse_lazy('home')
	template_name = 'login.html'

	def get_context_data(self, **kwargs):
		context = super(LoginView, self).get_context_data(**kwargs)
		context['form'] = UserLoginSerializer
		context['next'] = self.request.GET.get('next', '')
		return context

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			return HttpResponseRedirect(self.get_success_url())
		else:
			return super(LoginView, self).dispatch(request, *args, **kwargs)
	
	def get_success_url(self):
		next = self.request.GET.get('next')
		if(next):
			url = next
		elif(self.success_url):
			url = force_text(self.success_url)
		return url


@method_decorator(login_required, name='dispatch')
class LogoutView(RedirectView):
	url = reverse_lazy('login')

	def get(self, request, *args, **kwargs):
		logout(request)
		messages.info(request, 'Ha salido del sistema')
		return super(LogoutView, self).get(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(posee_usuarios_a_cargo, redirect_field_name=reverse_lazy('home')), name='dispatch')
class UsersView(TemplateView):
	template_name = 'users.html'

	def get_context_data(self, **kwargs):
		context = super(UsersView, self).get_context_data(**kwargs)
		context['serializer'] = UserCreateSerializer
		context['page_size'] = settings.FRONTEND_PAGE_SIZE
		context['update_serializer'] = UserRetrieveUpdateDestroySerializer
		return context