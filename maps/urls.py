from django.conf.urls import url

from maps.views import region

urlpatterns = [
    url(r'^(?P<id>\w+)/$', region, name='region'),
]