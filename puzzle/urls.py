from django.conf.urls import url

from puzzle.views import WorkshopView, questions, puzzle, PuzzleEditView


urlpatterns = [
    url(r'^(?P<name>[a-zA-Z0-9_]+)/questions/$', questions, name='puzzle_questions'),
    url(r'^workshop/$', WorkshopView.as_view(), name='workshop'),
    url(r'^(?P<name>[a-zA-Z0-9_]+)/$', puzzle, name='puzzle_map'),
    url(r'^(?P<name>[a-zA-Z0-9_]+)/edit/$', PuzzleEditView.as_view(), name='puzzle_edit'),
]
