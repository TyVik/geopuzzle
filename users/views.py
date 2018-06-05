from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView as DefaultLoginView
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import FormView
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import BaseUpdateView

from users.forms import AuthenticationForm, RegistrationForm, ProfileForm
from users.models import User


class LoginView(DefaultLoginView):
    form_class = AuthenticationForm


class RegistrationView(FormView):
    form_class = RegistrationForm
    template_name = 'registration/registration.html'
    success_url = '/accounts/profile/'

    def form_valid(self, form: RegistrationForm) -> HttpResponse:
        user = form.save(language=self.request.LANGUAGE_CODE)
        auth_login(self.request, user, 'django.contrib.auth.backends.ModelBackend')
        return HttpResponseRedirect(self.get_success_url())


class ProfileView(TemplateResponseMixin, BaseUpdateView):
    form_class = ProfileForm
    template_name = 'user/profile.html'
    success_url = '/accounts/profile/'
    model = User

    def get_object(self, queryset=None) -> User:
        return self.request.user
