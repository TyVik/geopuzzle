from django.conf.urls import url, include

from users.views import LoginView, RegistrationView, ProfileView

urlpatterns = [
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(r'^profile/puzzle/$', ProfileView.as_view(), name='puzzle_edit'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^registration/$', RegistrationView.as_view(), name='registration'),
    url(r'social', include('social_django.urls', namespace='social')),
    url(r'', include('django.contrib.auth.urls')),
]
