from awesome_avatar.forms import AvatarField
from django import forms
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm as DefaultAuthenticationForm, UsernameField
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from users.models import User


class AuthenticationForm(DefaultAuthenticationForm):
    username = UsernameField(label=_("Username"), max_length=150,
                             widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegistrationForm(forms.Form):
    username = UsernameField(label=_("Username"), max_length=150,
                             widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_username(self) -> str:
        username = self.cleaned_data['username'].lower()
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already has been used")
        return username

    def clean_email(self) -> str:
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already has been used")
        return email

    def save(self, language: str) -> User:
        self.cleaned_data['language'] = language if language in settings.ALLOWED_LANGUAGES else 'en'
        return User.objects.create_user(**self.cleaned_data)


class CustomAvatarField(AvatarField):
    def run_validators(self, value):
        pass


class ProfileForm(ModelForm):
    image = CustomAvatarField(label=_('Avatar'))

    class Meta:
        model = User
        fields = ('email', 'image', 'language')

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    def as_row(self):
        return self._html_output(
            normal_row='<dl class="form-group"><dt>%(label)s</dt><dd>%(field)s</dd>%(help_text)s</dl>',
            error_row='<li>%s</li>',
            row_ender='</dl>',
            help_text_html=' <span class="helptext">%s</span>',
            errors_on_separate_row=False
        )


class AvatarChangeForm(ModelForm):
    class Meta:
        model = User
        fields = ('image',)
