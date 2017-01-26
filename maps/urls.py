from django.conf.urls import url

from maps import views

urlpatterns = [
    url(r'^infobox/(?P<pk>[a-zA-Z0-9]+)', views.infobox, name='maps_infobox'),
    url(r'^questions/(?P<name>[a-zA-Z0-9]+)', views.questions, name='maps_questions'),
    url(r'^(?P<name>[a-zA-Z0-9]+)', views.maps, name='maps_map'),
]
