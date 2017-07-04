from django.conf.urls import url

from puzzle import views


urlpatterns = [
    url(r'^questions/(?P<name>[a-zA-Z0-9]+)/$', views.questions, name='puzzle_questions'),
    url(r'^(?P<name>[a-zA-Z0-9]+)/$', views.puzzle, name='puzzle_map'),
]
