from django.conf.urls import url, include

from maps import views

area_patterns = [
    url(r'^(?P<pk>\d+)/infobox/', views.infobox_by_id, name='infobox_by_id'),
]

urlpatterns = [
    url(r'^react/', views.react, name='maps_react'),
    url(r'^area/', include(area_patterns)),
    url(r'^infobox/(?P<pk>[a-zA-Z0-9]+)', views.infobox, name='maps_infobox'),
    url(r'^questions/(?P<name>[a-zA-Z0-9]+)', views.questions, name='maps_questions'),
    url(r'^(?P<name>[a-zA-Z0-9]+)', views.maps, name='maps_map'),
]
