from common.views import GameView, QuestionView
from .forms import QuizInfoboxForm
from .models import Quiz


class QuizQuestionView(QuestionView):
    model = Quiz
    form = QuizInfoboxForm


class QuizView(GameView):
    model = Quiz
    template = 'quiz/map.html'
