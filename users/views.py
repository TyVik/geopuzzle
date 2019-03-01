from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView as DefaultLoginView
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
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
    form_classes = {
        'main': ProfileForm,
        'password': PasswordChangeForm
    }
    template_name = 'user/profile.html'
    success_url = '/accounts/profile/'
    model = User

    def get_context_data(self, **kwargs):
        kwargs['form'] = ProfileForm(instance=self.object)
        connected_providers = list(self.object.social_auth.values_list('provider', flat=True))
        kwargs['providers'] = [{'slug': key, 'connected': key in connected_providers, **value} for key, value in settings.BACKEND_DESCRIBERS.items()]
        return super(ProfileView, self).get_context_data(**kwargs)

    def form_invalid(self, form):
        return JsonResponse(form.errors)

    def form_valid(self, form):
        form.save()
        if isinstance(form, PasswordChangeForm):
            auth_login(self.request, self.object, 'django.contrib.auth.backends.ModelBackend')
        return JsonResponse({})

    def get_form_class(self):
        return self.form_classes.get(self.request.GET.get('section'))

    def get_form_kwargs(self):
        result = super(ProfileView, self).get_form_kwargs()
        if self.request.GET.get('section') == 'password':
            result['user'] = self.object
            del result['instance']
        return result

    def get_object(self, queryset=None) -> User:
        return self.request.user
