import base64

from django import forms
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm as DefaultAuthenticationForm, UsernameField
from django.core.files.base import ContentFile
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from common.utils import random_string
from users.models import User


class AuthenticationForm(DefaultAuthenticationForm):
    username = UsernameField(label=_("Username"), max_length=150,
                             widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UsernameEmailValidation:
    def clean_username(self) -> str:
        username = self.cleaned_data['username'].lower()
        if (self.initial.get('username') != username) and User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already has been used")
        return username

    def clean_email(self) -> str:
        email = self.cleaned_data['email'].lower()
        if (self.initial.get('email') != email) and User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already has been used")
        return email


class RegistrationForm(UsernameEmailValidation, forms.Form):
    username = UsernameField(label=_("Username"), max_length=150,
                             widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def save(self, language: str) -> User:
        self.cleaned_data['language'] = language if language in settings.ALLOWED_LANGUAGES else 'en'
        return User.objects.create_user(**self.cleaned_data)


class ProfileForm(UsernameEmailValidation, ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'language', 'is_subscribed', 'image')

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False

    def clean_image(self):
        value = self.data['image']
        if ';base64,' in value:
            format, imgstr = value.split(';base64,')
            ext = format.split('/')[-1]

            return ContentFile(base64.b64decode(imgstr), name=f'{random_string()}.{ext}')
        return value.replace('/upload/', '')
