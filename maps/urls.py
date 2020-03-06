from django.conf.urls import url
from django.views.decorators.cache import cache_page

from common.constants import DAY
from .views import region, index_scroll

urlpatterns = [
    url(r'^regions/(?P<pk>\w+)/$', cache_page(DAY)(region), name='region'),
    url(r'^index/scroll/(?P<game>\w+)/$', index_scroll, name='index_scroll')
]
