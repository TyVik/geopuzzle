from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from users.views import LoginView, RegistrationView, ProfileView

urlpatterns = [
    url(r'^profile/$', login_required(ProfileView.as_view()), name='profile'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^registration/$', RegistrationView.as_view(), name='registration'),
    url(r'^social/', include('social_django.urls', namespace='social')),
    url(r'', include('django.contrib.auth.urls')),
]
