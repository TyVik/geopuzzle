from django.urls import path
from django.views.decorators.cache import cache_page

from common.constants import DAY
from .views import region, index_scroll

urlpatterns = [
    path('regions/<int:pk>/', cache_page(DAY)(region), name='region'),
    path('index/scroll/<game>/', index_scroll, name='index_scroll')
]
