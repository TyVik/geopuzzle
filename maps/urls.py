from django.conf.urls import url

from maps import views

urlpatterns = [
    url(r'^$', views.index, name='maps_index'),
    url(r'^(?P<name>[a-zA-Z0-9]+)', views.maps, name='maps_map'),
]
