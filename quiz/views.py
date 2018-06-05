from django.conf import settings
from django.utils.translation import ugettext as _

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import never_cache

from quiz.forms import QuizInfoboxForm
from quiz.models import Quiz


@never_cache
def questions(request: WSGIRequest, name: str) -> JsonResponse:
    request._cache_update_cache = False  # disable internal cache
    quiz = get_object_or_404(Quiz, slug=name)
    form = QuizInfoboxForm(data=request.GET, game=quiz)
    if not form.is_valid():
        return JsonResponse(form.errors, status=400)
    return JsonResponse(form.json())


def quiz(request: WSGIRequest, name: str) -> HttpResponse:
    quiz = get_object_or_404(Quiz, slug=name)
    trans = quiz.load_translation(request.LANGUAGE_CODE)
    context = {
        'language': request.LANGUAGE_CODE,
        'game': quiz,
        'name': trans.name,
        'text': _('Quiz \"{name}\" has been solved! You guessed all {subjects}. Your time is ').format(
            name=trans.name if quiz.id != 1 else _('World map'),
            subjects=_('countries') if quiz.is_global else _('regions'))
    }
    return render(request, 'quiz/map.html', context=context)
