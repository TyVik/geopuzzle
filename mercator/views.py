from django.http import HttpResponsePermanentRedirect
from django.urls import reverse
from django.utils.translation import ugettext as _

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render

from puzzle.models import Puzzle
from quiz.models import Quiz


def index(request: WSGIRequest) -> HttpResponse:
    puzzles = Puzzle.objects.filter(translations__language_code=request.LANGUAGE_CODE, is_published=True).order_by('translations__name').all()
    quizzes = Quiz.objects.filter(translations__language_code=request.LANGUAGE_CODE, is_published=True).order_by('translations__name').all()
    games = [{
        'items': {
            'parts': puzzles.filter(is_global=True),
            'countries': puzzles.filter(is_global=False)
        },
        'name': 'puzzle',
        'link': 'puzzle_map',
        'caption': _('puzzle'),
        'rules': _('In the Puzzle you need to drag the shape of the territory to the right place. Just like in childhood we collected pictures piece by piece, so here you can collect a country from regions or whole continents from countries!')
    }, {
        'items': {
            'parts': quizzes.filter(is_global=True),
            'countries': quizzes.filter(is_global=False)
        },
        'name': 'quiz',
        'link': 'quiz_map',
        'caption': _('quiz'),
        'rules': _('In the Quiz you need find the country by flag, emblem or the capital. Did you know that Monaco and Indonesia have the same flags? And that the flags of the United States and Liberia differ only in the number of stars? So, these and other interesting things can be learned and remembered after brainstorming right now!')
    }]
    return render(request, 'index.html', {'games': games})


def deprecated_redirect(request: WSGIRequest, name: str) -> HttpResponsePermanentRedirect:
    return HttpResponsePermanentRedirect(reverse('puzzle_map', kwargs={'name': name}))
