from django.conf.urls import url

from puzzle import views


urlpatterns = [
    url(r'^questions/(?P<name>[a-zA-Z0-9_]+)/$', views.questions, name='puzzle_questions'),
    url(r'^(?P<name>[a-zA-Z0-9_]+)/$', views.puzzle, name='puzzle_map'),
    url(r'^(?P<name>[a-zA-Z0-9_]+)/edit/$', views.PuzzleEditView.as_view(), name='puzzle_edit'),
]
