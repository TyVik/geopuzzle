from django.conf.urls import url

from .views import PuzzleView, PuzzleQuestionView

urlpatterns = [
    url(r'^(?P<name>[a-zA-Z0-9_]+)/questions/$', PuzzleQuestionView.as_view(), name='puzzle_questions'),
    url(r'^(?P<name>[a-zA-Z0-9_]+)/$', PuzzleView.as_view(), name='puzzle_map'),
]
