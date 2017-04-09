from django.utils.translation import ugettext as _

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from maps.models import Country
from quiz.forms import QuizInfoboxForm


def questions(request: WSGIRequest, name: str) -> JsonResponse:
    form = QuizInfoboxForm(data=request.GET, country=name, lang=request.LANGUAGE_CODE)
    if not form.is_valid():
        return JsonResponse(form.errors, status=400)
    return JsonResponse(form.json(), safe=False)


def quiz(request: WSGIRequest, name: str) -> HttpResponse:
    country = get_object_or_404(Country, slug=name)
    context = {
        'language': request.LANGUAGE_CODE,
        'country': country,
        'text': _('{name} has been studied! You guessed all {subjects}. You time is ').format(
            name=country.name if country.id != 1 else _('World map'),
            subjects=_('countries') if country.is_global else _('regions'))
    }
    return render(request, 'quiz/map.html', context=context)
