from django.conf.urls import url, include

from users.views import LoginView, RegistrationView, ProfileView

urlpatterns = [
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^registration/$', RegistrationView.as_view(), name='registration'),
    url(r'', include('django.contrib.auth.urls')),
]
