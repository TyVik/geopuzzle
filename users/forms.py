from django import forms
from django.contrib.auth.forms import AuthenticationForm as DefaultAuthenticationForm, UsernameField
from django.utils.translation import ugettext_lazy as _

from users.models import User


class AuthenticationForm(DefaultAuthenticationForm):
    username = UsernameField(max_length=150, widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegistrationForm(forms.Form):
    username = UsernameField(max_length=150, widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already has been used")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already has been used")
        return email

    def save(self):
        return User.objects.create_user(**self.cleaned_data)
