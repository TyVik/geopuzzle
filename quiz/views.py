from typing import Dict

from django.contrib.gis.geos import Point
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from maps.models import Country, Area
from maps.views import MapForm


def quiz_area(area: Area) -> Dict:
    return {'success': True, 'infobox': area.strip_infobox, 'polygon': area.polygon_gmap}


@csrf_exempt
def check(request: WSGIRequest, pk: str) -> JsonResponse:
    area = get_object_or_404(Area, pk=pk)
    lat = request.POST.get('lat', None)
    lng = request.POST.get('lng', None)
    lat, lng = float(lat), float(lng)
    if area.polygon.contains(Point(lng, lat)):
        return JsonResponse(quiz_area(area))
    return JsonResponse({'success': False})


def giveup(request: WSGIRequest, pk: str) -> JsonResponse:
    area = get_object_or_404(Area, pk=pk)
    return JsonResponse(quiz_area(area))


def questions(request: WSGIRequest, name: str) -> JsonResponse:
    params = request.GET.copy()
    params['country'] = name
    params['lang'] = request.LANGUAGE_CODE
    form = MapForm(params)
    if not form.is_valid():
        return JsonResponse(form.errors, status=400)
    result = [{
        'id': area.id,
        'name': area.name,
        'flag': area.infobox.get('flag', None),
        'coat_of_arms': area.infobox.get('coat_of_arms', None),
        'capital': area.infobox['capital']['name'] if 'capital' in area.infobox else None
    } for area in form.areas()]
    return JsonResponse(result, safe=False)


def quiz(request: WSGIRequest, name: str) -> HttpResponse:
    country = get_object_or_404(Country, slug=name)
    context = {
        'language': request.LANGUAGE_CODE,
        'country': country,
    }
    return render(request, 'quiz/map.html', context=context)


def index(request: WSGIRequest) -> HttpResponse:
    query = Country.objects.language(request.LANGUAGE_CODE).filter(is_published=True).order_by('name').all()
    parts = query.filter(is_global=True)
    countries = query.filter(is_global=False)
    return render(request, 'index.html', {'countries': countries, 'parts': parts})
