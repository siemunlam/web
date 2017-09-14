# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView

from medicos.models import Medico

# Create your views here.
class LoginView(FormView):
	form_class = AuthenticationForm
	success_url = reverse_lazy('home')
	template_name = 'login.html'

	@method_decorator(sensitive_post_parameters('password'))
	@method_decorator(csrf_protect)
	@method_decorator(never_cache)
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			return HttpResponseRedirect(self.get_success_url())
		else:
			# Sets a test cookie to make sure the user has cookies enabled
			request.session.set_test_cookie()
			return super(LoginView, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		if Medico.objects.filter(usuario=form.get_user()).exists():
			messages.error(self.request, u'No se permite ingresar a los médicos', extra_tags='danger')
			return super(LoginView, self).form_invalid(form)
		login(self.request, form.get_user())
		# If the test cookie worked, go ahead and
		# delete it since its no longer needed
		if self.request.session.test_cookie_worked():
			self.request.session.delete_test_cookie()
		return super(LoginView, self).form_valid(form)

	def get_success_url(self):
		next = self.request.GET.get('next')
		if(next):
			url = next
		elif(self.success_url):
			url = force_text(self.success_url)
		return url


class LogoutView(RedirectView):
	url = reverse_lazy('login')

	def get(self, request, *args, **kwargs):
		logout(request)
		messages.info(request, 'Ha salido del sistema')
		return super(LogoutView, self).get(request, *args, **kwargs)