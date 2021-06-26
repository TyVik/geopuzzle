from django.urls import include, path
from django.contrib.auth.decorators import login_required

from .views import LoginView, RegistrationView, ProfileView, UserView

urlpatterns = [
    path('profile/', login_required(ProfileView.as_view()), name='profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('social/', include('social_django.urls', namespace='social')),
    path('users/', UserView.as_view(), name='users'),
    path('', include('django.contrib.auth.urls')),
]
