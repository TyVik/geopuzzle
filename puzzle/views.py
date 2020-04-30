from common.views import GameView, QuestionView
from .forms import PuzzleForm
from .models import Puzzle


class PuzzleQuestionView(QuestionView):
    model = Puzzle
    form = PuzzleForm


class PuzzleView(GameView):
    model = Puzzle
    template = 'puzzle/map.html'
