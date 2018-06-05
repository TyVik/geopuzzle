from django.conf.urls import url

from maps.views import region, items

urlpatterns = [
    url(r'^(?P<id>\w+)/$', region, name='region'),
    url(r'^(?P<id>\w+)/items/$', items, name='region_items'),
]