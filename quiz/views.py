from django.conf import settings
from django.utils.translation import ugettext as _

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from quiz.forms import QuizInfoboxForm
from quiz.models import Quiz


def questions(request: WSGIRequest, name: str) -> JsonResponse:
    quiz = get_object_or_404(Quiz, slug=name)
    form = QuizInfoboxForm(data=request.GET, game=quiz, lang=request.LANGUAGE_CODE)
    if not form.is_valid():
        return JsonResponse(form.errors, status=400)
    return JsonResponse(form.json(), safe=False)


def quiz(request: WSGIRequest, name: str) -> HttpResponse:
    quiz = get_object_or_404(Quiz, slug=name)
    context = {
        'google_key': settings.GOOGLE_KEY,
        'language': request.LANGUAGE_CODE,
        'country': quiz,
        'text': _('{name} has been studied! You guessed all {subjects}. You time is ').format(
            name=quiz.name if quiz.id != 1 else _('World map'),
            subjects=_('countries') if quiz.is_global else _('regions'))
    }
    return render(request, 'quiz/map.html', context=context)
