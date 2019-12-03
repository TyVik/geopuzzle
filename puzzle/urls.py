from django.conf.urls import url

from .views import questions, puzzle

urlpatterns = [
    url(r'^(?P<name>[a-zA-Z0-9_]+)/questions/$', questions, name='puzzle_questions'),
    url(r'^(?P<name>[a-zA-Z0-9_]+)/$', puzzle, name='puzzle_map'),
]
