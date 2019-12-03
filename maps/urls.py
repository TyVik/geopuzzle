from django.conf.urls import url
from django.views.decorators.cache import cache_page

from common.constants import DAY
from .views import region, items

urlpatterns = [
    url(r'^(?P<pk>\w+)/$', cache_page(DAY)(region), name='region'),
    url(r'^(?P<pk>\w+)/items/$', cache_page(DAY)(items), name='region_items'),
]