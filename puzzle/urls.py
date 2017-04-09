from django.conf.urls import url, include

from puzzle import views

area_patterns = [
    url(r'^(?P<pk>\d+)/infobox/', views.infobox_by_id, name='infobox_by_id'),
]


urlpatterns = [
    url(r'^area/', include(area_patterns)),
    url(r'^questions/(?P<name>[a-zA-Z0-9]+)/$', views.questions, name='puzzle_questions'),
    url(r'^(?P<name>[a-zA-Z0-9]+)/$', views.puzzle, name='puzzle_map'),
]
