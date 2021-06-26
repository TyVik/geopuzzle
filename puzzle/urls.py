from django.urls import path

from .views import PuzzleView, PuzzleQuestionView

urlpatterns = [
    path('<name>/questions/', PuzzleQuestionView.as_view(), name='puzzle_questions'),
    path('<name>/', PuzzleView.as_view(), name='puzzle_map'),
]
