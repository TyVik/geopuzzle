from django.utils.translation import ugettext as _

from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import never_cache

from common.middleware import WSGILanguageRequest
from .forms import QuizInfoboxForm
from .models import Quiz


@never_cache
def questions(request: WSGILanguageRequest, name: str) -> JsonResponse:
    request._cache_update_cache = False  # disable internal cache pylint: disable=protected-access
    obj = get_object_or_404(Quiz, slug=name)
    form = QuizInfoboxForm(data=request.GET, game=obj)
    if not form.is_valid():
        return JsonResponse(form.errors, status=400)
    return JsonResponse(form.json())


def quiz(request: WSGILanguageRequest, name: str) -> HttpResponse:
    obj = get_object_or_404(Quiz, slug=name)
    trans = obj.load_translation(request.LANGUAGE_CODE)
    context = {
        'game': obj,
        'name': trans.name,
        'text': _('Quiz \"{name}\" has been solved! You guessed all {subjects}. Your time is ').format(
            name=trans.name if obj.pk != 1 else _('World map'),
            subjects=_('countries') if obj.is_global else _('regions'))
    }
    return render(request, 'quiz/map.html', context=context)
