from django.conf.urls import url
from django.views.decorators.cache import cache_page

from common.constants import DAY
from .views import region

urlpatterns = [
    url(r'^(?P<pk>\w+)/$', cache_page(DAY)(region), name='region'),
]