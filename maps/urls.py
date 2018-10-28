from django.conf.urls import url
from django.views.decorators.cache import cache_page

from common.constants import DAY
from maps.views import region, items

urlpatterns = [
    url(r'^(?P<id>\w+)/$', cache_page(DAY)(region), name='region'),
    url(r'^(?P<id>\w+)/items/$', cache_page(DAY)(items), name='region_items'),
]