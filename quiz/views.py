from typing import Dict

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from maps.models import Country, Area
from quiz.forms import PointContainsForm, QuizInfoboxForm


def quiz_area(area: Area) -> Dict:
    return {'success': True, 'infobox': area.strip_infobox, 'polygon': area.polygon_gmap}


@csrf_exempt
def check(request: WSGIRequest, pk: str) -> JsonResponse:
    area = get_object_or_404(Area, pk=pk)
    form = PointContainsForm(request.POST, area=area)
    result = quiz_area(area) if form.is_valid() else {'success': False}
    return JsonResponse(result)


def giveup(request: WSGIRequest, pk: str) -> JsonResponse:
    area = get_object_or_404(Area, pk=pk)
    return JsonResponse(quiz_area(area))


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
    }
    return render(request, 'quiz/map.html', context=context)
