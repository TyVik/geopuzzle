from __future__ import annotations

from typing import Union, Type, Literal, Dict

from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView as DefaultLoginView
from django.db.models import QuerySet
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.generic import FormView
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import BaseUpdateView
from django.views.generic.list import BaseListView

from common.middleware import WSGILanguageRequest
from common.views import AutocompleteItem
from .filters import UserFilter
from .forms import AuthenticationForm, RegistrationForm, ProfileForm
from .models import User


class LoginView(DefaultLoginView):
    form_class = AuthenticationForm


class RegistrationView(FormView):
    request: WSGILanguageRequest
    form_class = RegistrationForm
    template_name = 'registration/registration.html'
    success_url = '/accounts/profile/'

    def form_valid(self, form: RegistrationForm) -> HttpResponse:
        user = form.save(language=self.request.LANGUAGE_CODE)
        auth_login(self.request, user, 'django.contrib.auth.backends.ModelBackend')
        return HttpResponseRedirect(self.get_success_url())


ProfileForms = Union[ProfileForm, PasswordChangeForm]
ProfileSection = Literal['main', 'password']


class ProfileView(TemplateResponseMixin, BaseUpdateView):
    form_classes: Dict[ProfileSection, Type[ProfileForms]] = {
        'main': ProfileForm,
        'password': PasswordChangeForm
    }
    template_name = 'user/profile.html'
    success_url = '/accounts/profile/'
    model = User
    object: User

    def get_context_data(self, **kwargs) -> dict:
        kwargs['form'] = ProfileForm(instance=self.object)
        connected_providers = list(self.object.social_auth.values_list('provider', flat=True))
        kwargs['providers'] = [{'slug': key, 'connected': key in connected_providers, **value}
                               for key, value in settings.BACKEND_DESCRIBERS.items()]
        return super(ProfileView, self).get_context_data(**kwargs)

    def form_invalid(self, form: ProfileForms) -> JsonResponse:
        return JsonResponse(form.errors, status=400)

    def form_valid(self, form: ProfileForms) -> JsonResponse:
        form.save()
        if isinstance(form, PasswordChangeForm):
            auth_login(self.request, self.object, 'django.contrib.auth.backends.ModelBackend')
        return JsonResponse({})

    def _get_section(self) -> ProfileSection:
        return self.request.GET.get('section', 'main')

    def get_form_class(self) -> Type[ProfileForms]:
        return self.form_classes[self._get_section()]

    def get_form_kwargs(self) -> dict:
        result = super(ProfileView, self).get_form_kwargs()
        if self._get_section() == 'password':
            result['user'] = self.object
            del result['instance']
        return result

    def get_object(self, queryset: QuerySet[User] = None) -> User:
        return self.request.user


class UserView(BaseListView):
    model = User

    def get_queryset(self) -> QuerySet[User]:
        return UserFilter(self.request.GET, super(UserView, self).get_queryset()).qs

    @staticmethod
    def convert_item(item: User) -> AutocompleteItem:
        return {'value': str(item.pk), 'label': item.username}

    def render_to_response(self, context, **kwargs) -> JsonResponse:
        return JsonResponse([self.convert_item(item) for item in context['object_list']], safe=False)
